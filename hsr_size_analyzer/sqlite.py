import sqlite3
from typing import Dict, Any, Literal, Tuple

import duckdb
import pandas as pd

from hsr_size_analyzer.logger_config import main_logger


def create_proportion_query(group_by_column: str) -> str:
    return f'''
    WITH TotalSize AS (
        SELECT SUM(COALESCE(Size, 0)) AS totalSize
        FROM df
    )
    SELECT
        {group_by_column},
        SUM(COALESCE(Size, 0)) / CAST(ts.totalSize AS DECIMAL) * 100 AS Proportion
    FROM
        df,
        TotalSize AS ts
    GROUP BY
        {group_by_column}, ts.totalSize;
    '''


def execute_duckdb_query(query: str, df: pd.DataFrame) -> pd.DataFrame:
    """
    Execute a query using DuckDB and a provided DataFrame.

    :param query: The SQL query to be executed.
    :param df: DataFrame to be used in the query.
    :return: DataFrame containing the result after executing the query.
    """
    con = duckdb.connect(':memory:')

    # Register the DataFrame
    con.register('df', df)
    result = con.execute(query).fetchdf()
    con.close()
    return result


def get_data_type() -> Dict[str, str]:
    return {
        'Extension': 'text',
        'Size': 'real',
        'Directory': 'text',
        'Proportion': 'real',
        'Full Path': 'text'
    }


def write_to_sqlite(conn: sqlite3.Connection,
                    df: pd.DataFrame,
                    table_name: str,
                    if_exists: Literal["fail", "replace", "append"] = 'replace',
                    dtype: Dict[str, Any] = None) -> None:
    """
    Write a DataFrame to an SQLite database table.

    :param conn: Connection to the SQLite database.
    :param df: DataFrame to be written to the database.
    :param table_name: Name of the table to write the DataFrame to.
    :param if_exists: Action to take if the table already exists ('fail', 'replace', or 'append').
    :param dtype: Dictionary mapping column names to SQL types.
    :return: None
    """
    df.to_sql(table_name, con=conn, if_exists=if_exists, dtype=dtype)


def analyze_data(df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Analyze the data in the DataFrame by calculating the proportion based on file extensions and directories.

    :param df: DataFrame containing the data to be analyzed.
    :return: A tuple of two DataFrames representing the analysis results for file extensions and directories.
    """
    file_ext_df = execute_duckdb_query(create_proportion_query('Extension'), df)
    file_dir_df = execute_duckdb_query(create_proportion_query('Directory'), df)
    return file_ext_df, file_dir_df


def save_analysis_to_db(df: pd.DataFrame, file_ext_df: pd.DataFrame, file_dir_df: pd.DataFrame,
                        db: str = 'hsr_size_analyzer.db') -> None:
    """
    Save the analysis results to an SQLite database.

    :param df: DataFrame containing the original data.
    :param file_ext_df: DataFrame with file extension analysis results.
    :param file_dir_df: DataFrame with directory analysis results.
    :param db: Name of the SQLite database file to save the analysis results (default is 'hsr_size_analyzer.db').
    :return: None
    """
    try:
        with sqlite3.connect(db) as conn:
            write_to_sqlite(conn, df, 'HsrSizeAnalysis', dtype=get_data_type())
            write_to_sqlite(conn, file_ext_df, 'HsrSizeDist')
            write_to_sqlite(conn, file_dir_df, 'HsrDirDist')
    except sqlite3.OperationalError as e:
        main_logger.error(f"OperationalError during saving to database {db}: {e}", exc_info=True)
        conn.rollback()
    except Exception as e:
        main_logger.error(f"Unexpected error during saving to database {db}: {e}", exc_info=True)
        conn.rollback()


def save_to_db(df: pd.DataFrame, db: str = 'hsr_size_analyzer.db') -> None:
    """
    Save the DataFrame to an SQLite database after analyzing the data based on file extensions and directories.

    :param df: DataFrame containing the data to be saved and analyzed.
    :param db: Name of the SQLite database file to save the analysis results (default is 'hsr_size_analyzer.db').
    :return: None
    """
    file_ext_df, file_dir_df = analyze_data(df)

    try:
        save_analysis_to_db(df, file_ext_df, file_dir_df, db)
    except sqlite3.OperationalError as e:
        main_logger.error(f"OperationalError during saving to database {db}: {e}", exc_info=True)
    except Exception as e:
        main_logger.error(f"Unexpected error during saving to database {db}: {e}", exc_info=True)