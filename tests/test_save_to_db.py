import sqlite3

import pandas as pd

from hsr_size_analyzer.sqlite import save_to_db


def test_save_dataframe_to_sqlite_successfully():
    # Create a sample DataFrame
    data = {
        'Extension': ['.txt', '.jpg', '.png'],
        'Size': [100, 200, 300],
        'Directory': ['/home/user/docs', '/home/user/images', '/home/user/images'],
        'Full Path': ['/home/user/docs/file1.txt', '/home/user/images/file2.jpg', '/home/user/images/file3.png']
    }
    df = pd.DataFrame(data)
    db = 'test_save_dataframe_to_sqlite_successfully.db'

    # Call the function to save the DataFrame to the SQLite database
    save_to_db(df, db=db)

    # Verify that the tables have been created and contain the expected data
    with sqlite3.connect(db) as conn:
        cursor = conn.cursor()

        # Check HsrSizeAnalysis table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HsrSizeAnalysis';")
        assert cursor.fetchone() is not None

        # Check HsrSizeDist table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HsrSizeDist';")
        assert cursor.fetchone() is not None

        # Check HsrDirDist table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='HsrDirDist';")
        assert cursor.fetchone() is not None