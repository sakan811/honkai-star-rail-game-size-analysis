import sqlite3
from typing import Dict, Any, Literal

import duckdb
import pandas as pd


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

    :param query: The SQL query to execute.
    :param df: The DataFrame to be used in the query.
    :return: The result DataFrame after executing the query.
    """
    # Create a DuckDB connection and register the DataFrame
    con = duckdb.connect(':memory:')
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


def save_to_db(df: pd.DataFrame, db: str = 'hsr_size_analyzer.db') -> None:
    """
    Save DataFrame to an SQLite database after analyzing file sizes by extension and directory.

    :param db: SQLite database file path.
                Default is 'hsr_size_analyzer.db'
    :param df: DataFrame containing file size data.
    :return: None
    """
    file_ext_df = execute_duckdb_query(create_proportion_query('Extension'), df)
    file_dir_df = execute_duckdb_query(create_proportion_query('Directory'), df)

    with sqlite3.connect(db) as conn:
        write_to_sqlite(conn, df, 'HsrSizeAnalysis', dtype=get_data_type())
        write_to_sqlite(conn, file_ext_df, 'HsrSizeDist')
        write_to_sqlite(conn, file_dir_df, 'HsrDirDist')