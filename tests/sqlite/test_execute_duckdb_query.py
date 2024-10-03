import duckdb
import pandas as pd
import pytest

from hsr_size_analyzer.sqlite import execute_duckdb_query

@pytest.fixture
def duckdb_con():
    return duckdb.connect(':memory:')


# Executes a valid SQL query on a provided DataFrame
def test_execute_valid_query(duckdb_con):
    query = "SELECT * FROM df"
    data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    df = pd.DataFrame(data)
    result = execute_duckdb_query(query, df)
    assert result.equals(df)


# Successfully registers the DataFrame in DuckDB
def test_successfully_registers_dataframe(duckdb_con):
    query = "SELECT * FROM df"
    data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    df = pd.DataFrame(data)
    result = execute_duckdb_query(query, df)
    assert result.equals(df)


# Returns a DataFrame with the expected results
def test_returns_expected_dataframe(duckdb_con):
    query = "SELECT * FROM df"
    data = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    df = pd.DataFrame(data)
    result = execute_duckdb_query(query, df)
    expected_result = pd.DataFrame(data)
    pd.testing.assert_frame_equal(result, expected_result)


# Handles an empty DataFrame
def test_handles_empty_dataframe(duckdb_con):
    query = "SELECT * FROM df"
    df = pd.DataFrame()
    with pytest.raises(duckdb.InvalidInputException):
        execute_duckdb_query(query, df)


# Deals with DataFrame containing null values
def test_deals_with_dataframe_containing_null_values(duckdb_con):
    query = "SELECT * FROM df"
    df = pd.DataFrame({'A': [1, None, 3], 'B': [None, 5, 6]})
    result = execute_duckdb_query(query, df)
    assert result.equals(df)


# Handles DataFrame with special characters in column names
def test_handles_dataframe_with_special_characters(duckdb_con):
    query = "SELECT `column@#` FROM df"
    data = {'column@#': [1, 2, 3]}
    df = pd.DataFrame(data)
    with pytest.raises(duckdb.ParserException):
        execute_duckdb_query(query, df)
