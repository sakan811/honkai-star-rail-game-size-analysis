import pytest
import sqlite3
import pandas as pd
from io import StringIO

from hsr_size_analyzer.sqlite import write_to_sqlite


@pytest.fixture
def sample_data():
    data = StringIO('''
        Extension,Size,Directory,Full Path
        .txt,100,/home/user,/home/user/file1.txt
        .pdf,200,/home/user/documents,/home/user/documents/file2.pdf
        .jpg,150,/home/user/pictures,/home/user/pictures/file3.jpg
    ''')
    df = pd.read_csv(data, sep=',', skipinitialspace=True)
    return df


@pytest.fixture
def test_db_connection():
    conn = sqlite3.connect(':memory:')
    yield conn
    conn.close()


def test_write_to_sqlite_replace(sample_data, test_db_connection):
    write_to_sqlite(test_db_connection, sample_data, 'test_table', if_exists='replace')
    result = pd.read_sql_query("SELECT * FROM test_table", test_db_connection)
    assert len(result) == len(sample_data)
    assert set(sample_data.columns).issubset(set(result.columns))


def test_write_to_sqlite_append(sample_data, test_db_connection):
    write_to_sqlite(test_db_connection, sample_data, 'test_table', if_exists='replace')
    write_to_sqlite(test_db_connection, sample_data, 'test_table', if_exists='append')
    result = pd.read_sql_query("SELECT * FROM test_table", test_db_connection)
    assert len(result) == len(sample_data) * 2


def test_write_to_sqlite_fail(sample_data, test_db_connection):
    write_to_sqlite(test_db_connection, sample_data, 'test_table', if_exists='replace')
    with pytest.raises(ValueError):
        write_to_sqlite(test_db_connection, sample_data, 'test_table', if_exists='fail')


def test_write_to_sqlite_with_dtype(sample_data, test_db_connection):
    dtype = {'Extension': 'TEXT', 'Size': 'INTEGER', 'Directory': 'TEXT', 'Full Path': 'TEXT'}
    write_to_sqlite(test_db_connection, sample_data, 'test_table', if_exists='replace', dtype=dtype)

    cursor = test_db_connection.cursor()
    schema = cursor.execute("PRAGMA table_info(test_table)").fetchall()
    schema_dict = {row[1]: row[2] for row in schema}

    assert schema_dict['Extension'] == 'TEXT'
    assert schema_dict['Size'] == 'INTEGER'
    assert schema_dict['Directory'] == 'TEXT'
    assert schema_dict['Full Path'] == 'TEXT'
