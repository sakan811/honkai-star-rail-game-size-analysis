import sqlite3

import pandas as pd
from duckdb import duckdb


def save_to_db(df: pd.DataFrame, db: str = 'hsr_size_analyzer.db') -> None:
    """
    Save DataFrame to an SQLite database after analyzing file sizes by extension and directory.

    :param db: SQLite database file path.
                Default is 'hsr_size_analyzer.db'
    :param df: DataFrame containing file size data.
    :return: None
    """
    query = '''
    WITH TotalSize AS (
        SELECT SUM(COALESCE(Size, 0)) AS totalSize
        FROM df
    )
    SELECT
        Extension,
        SUM(COALESCE(Size, 0)) / CAST(ts.totalSize AS DECIMAL) * 100 AS Proportion
    FROM
        df,
        TotalSize AS ts
    GROUP BY
        Extension, ts.totalSize;
    '''
    file_ext_df = duckdb.sql(query).fetchdf()
    query = '''
    WITH TotalSize AS (
        SELECT SUM(COALESCE(Size, 0)) AS totalSize
        FROM df
    )
    SELECT
        Directory,
        SUM(COALESCE(Size, 0)) / CAST(ts.totalSize AS DECIMAL) * 100 AS Proportion
    FROM
        df,
        TotalSize AS ts
    GROUP BY
        Directory, ts.totalSize;
    '''
    file_dir_df = duckdb.sql(query).fetchdf()
    data_type = {
        'Extension': 'text',
        'Size': 'real',
        'Directory': 'text',
        'Proportion': 'real',
        'Full Path': 'text'
    }
    with sqlite3.connect(db) as conn:
        df.to_sql('HsrSizeAnalysis', con=conn, if_exists='replace', dtype=data_type)
        file_ext_df.to_sql('HsrSizeDist', con=conn, if_exists='replace')
        file_dir_df.to_sql('HsrDirDist', con=conn, if_exists='replace')
