import pytest
import pandas as pd
import sqlite3
from unittest.mock import patch, MagicMock, call

from hsr_size_analyzer.sqlite import save_analysis_to_db, get_data_type


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Extension': ['.txt', '.pdf'],
        'Size': [100, 200],
        'Directory': ['/home/user', '/home/user/documents'],
        'Full Path': ['/home/user/file1.txt', '/home/user/documents/file2.pdf']
    })


@pytest.fixture
def sample_file_ext_df():
    return pd.DataFrame({
        'Extension': ['.txt', '.pdf'],
        'Proportion': [33.33, 66.67]
    })


@pytest.fixture
def sample_file_dir_df():
    return pd.DataFrame({
        'Directory': ['/home/user', '/home/user/documents'],
        'Proportion': [33.33, 66.67]
    })


@patch('hsr_size_analyzer.sqlite.sqlite3.connect')
@patch('hsr_size_analyzer.sqlite.write_to_sqlite')
def test_save_analysis_to_db(mock_write_to_sqlite, mock_connect, sample_df, sample_file_ext_df, sample_file_dir_df):
    mock_conn = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conn

    save_analysis_to_db(sample_df, sample_file_ext_df, sample_file_dir_df, 'test.db')

    # Check if sqlite3.connect was called with the correct database name
    mock_connect.assert_called_once_with('test.db')

    # Check if write_to_sqlite was called three times with correct arguments
    assert mock_write_to_sqlite.call_count == 3

    expected_calls = [
        call(mock_conn, sample_df, 'HsrSizeAnalysis', dtype=get_data_type()),
        call(mock_conn, sample_file_ext_df, 'HsrSizeDist'),
        call(mock_conn, sample_file_dir_df, 'HsrDirDist')
    ]
    mock_write_to_sqlite.assert_has_calls(expected_calls, any_order=True)


@patch('hsr_size_analyzer.sqlite.sqlite3.connect')
@patch('hsr_size_analyzer.sqlite.write_to_sqlite')
def test_save_analysis_to_db_default_db_name(mock_write_to_sqlite, mock_connect, sample_df, sample_file_ext_df,
                                             sample_file_dir_df):
    mock_conn = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conn

    save_analysis_to_db(sample_df, sample_file_ext_df, sample_file_dir_df)

    # Check if sqlite3.connect was called with the default database name
    mock_connect.assert_called_once_with('hsr_size_analyzer.db')


@patch('hsr_size_analyzer.sqlite.sqlite3.connect')
@patch('hsr_size_analyzer.sqlite.write_to_sqlite')
def test_save_analysis_to_db_empty_dataframes(mock_write_to_sqlite, mock_connect):
    mock_conn = MagicMock()
    mock_connect.return_value.__enter__.return_value = mock_conn

    empty_df = pd.DataFrame()
    save_analysis_to_db(empty_df, empty_df, empty_df)

    # Check if write_to_sqlite was still called three times, even with empty DataFrames
    assert mock_write_to_sqlite.call_count == 3


@patch('hsr_size_analyzer.sqlite.sqlite3.connect')
@patch('hsr_size_analyzer.sqlite.write_to_sqlite', side_effect=sqlite3.Error("Database error"))
def test_save_analysis_to_db_database_error(mock_write_to_sqlite, mock_connect, sample_df, sample_file_ext_df,
                                            sample_file_dir_df):

    save_analysis_to_db(sample_df, sample_file_ext_df, sample_file_dir_df)

    # Check if sqlite3.connect was called
    mock_connect.assert_called_once()

    # Check if write_to_sqlite was called and raised the error
    mock_write_to_sqlite.assert_called_once()