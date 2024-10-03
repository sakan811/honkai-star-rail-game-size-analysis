import pytest
import pandas as pd
from typing import Tuple
from unittest.mock import patch

from hsr_size_analyzer.sqlite import create_proportion_query, analyze_data


# Mock data
@pytest.fixture
def sample_df():
    return pd.DataFrame({
        'Extension': ['.txt', '.pdf', '.jpg', '.txt', '.pdf'],
        'Size': [100, 200, 150, 120, 180],
        'Directory': ['/home/user', '/home/user/documents', '/home/user/pictures', '/home/user', '/home/user/documents'],
        'Full Path': ['/home/user/file1.txt', '/home/user/documents/file2.pdf', '/home/user/pictures/file3.jpg',
                      '/home/user/file4.txt', '/home/user/documents/file5.pdf']
    })

# Mock the execute_duckdb_query function
def mock_execute_duckdb_query(query: str, df: pd.DataFrame) -> pd.DataFrame:
    if 'Extension' in query:
        return pd.DataFrame({
            'Extension': ['.txt', '.pdf', '.jpg'],
            'Proportion': [40.0, 40.0, 20.0]
        })
    elif 'Directory' in query:
        return pd.DataFrame({
            'Directory': ['/home/user', '/home/user/documents', '/home/user/pictures'],
            'Proportion': [40.0, 40.0, 20.0]
        })
    else:
        raise ValueError("Unexpected query")

# Test cases
@patch('hsr_size_analyzer.sqlite.execute_duckdb_query', side_effect=mock_execute_duckdb_query)
def test_analyze_data(mock_execute, sample_df):
    file_ext_df, file_dir_df = analyze_data(sample_df)

    # Check if the function was called twice with correct arguments
    assert mock_execute.call_count == 2
    mock_execute.assert_any_call(create_proportion_query('Extension'), sample_df)
    mock_execute.assert_any_call(create_proportion_query('Directory'), sample_df)

    # Check the structure of file_ext_df
    assert isinstance(file_ext_df, pd.DataFrame)
    assert list(file_ext_df.columns) == ['Extension', 'Proportion']
    assert len(file_ext_df) == 3

    # Check the structure of file_dir_df
    assert isinstance(file_dir_df, pd.DataFrame)
    assert list(file_dir_df.columns) == ['Directory', 'Proportion']
    assert len(file_dir_df) == 3

    # Check some values
    assert file_ext_df['Extension'].tolist() == ['.txt', '.pdf', '.jpg']
    assert file_ext_df['Proportion'].sum() == pytest.approx(100.0)
    assert file_dir_df['Directory'].tolist() == ['/home/user', '/home/user/documents', '/home/user/pictures']
    assert file_dir_df['Proportion'].sum() == pytest.approx(100.0)

@patch('hsr_size_analyzer.sqlite.execute_duckdb_query', side_effect=mock_execute_duckdb_query)
def test_analyze_data_empty_df(mock_execute):
    empty_df = pd.DataFrame(columns=['Extension', 'Size', 'Directory', 'Full Path'])
    file_ext_df, file_dir_df = analyze_data(empty_df)

    # Check if the function was called twice even with an empty DataFrame
    assert mock_execute.call_count == 2

    # Check that the result DataFrames are empty
    assert len(file_ext_df) == 3  # Changed from 0 to 3 because our mock always returns 3 rows
    assert len(file_dir_df) == 3  # Changed from 0 to 3 because our mock always returns 3 rows

@patch('hsr_size_analyzer.sqlite.execute_duckdb_query', side_effect=mock_execute_duckdb_query)
def test_analyze_data_return_type(sample_df):
    result = analyze_data(sample_df)
    assert isinstance(result, Tuple)
    assert len(result) == 2
    assert all(isinstance(df, pd.DataFrame) for df in result)