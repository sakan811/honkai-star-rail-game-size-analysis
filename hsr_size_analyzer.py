import os
import sqlite3
from typing import Any
import duckdb

import pandas as pd
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_file_distribution(directory: str) -> pd.DataFrame:
    if '\\' in directory:
        directory = directory.replace('\\', '/')
    elif '\\\\' in directory:
        directory = directory.replace('\\\\', '/')

    # Ensure the directory ends with a backslash
    if not directory.endswith('/'):
        directory += '/'

    # Dictionary to store total size and a set of directories for each extension
    file_data: dict[str, list[Any]] = {
        'Extension': [],
        'Size': [],
        'Directory': [],
        'Full Path': []
    }
    total_size = 0

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[-1].lower()
            file_dir = root.replace(directory, '')
            transformed_file_path = file_path.replace(directory, '')

            if file_dir == '':
                file_dir = 'Root Directory'

            file_dir_list = file_dir.split(os.sep)
            file_dir_len = len(file_dir_list)

            if file_dir_len == 1:
                file_dir = file_dir_list[0]
            elif file_dir_len >= 2:
                file_dir = file_dir_list[1]

            if file_ext == '':
                file_ext = 'No extension'

            file_size = os.path.getsize(file_path)  # Get file size

            # Update total size
            total_size += file_size

            file_data['Extension'].append(file_ext)
            file_data['Size'].append(file_size)
            file_data['Directory'].append(file_dir)
            file_data['Full Path'].append(transformed_file_path)

    # Create a DataFrame from the extension data
    df = pd.DataFrame(file_data, columns=['Extension', 'Size', 'Directory', 'Full Path'])

    return df


if __name__ == "__main__":
    game_directory = os.getenv("GAME_DIR")
    df = get_file_distribution(game_directory)

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

    db = 'hsr_size_analyzer.db'
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
