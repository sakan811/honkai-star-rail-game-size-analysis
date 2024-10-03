from hsr_size_analyzer.sqlite import create_proportion_query


# Correctly calculates the proportion of each group in the dataset
def test_calculate_proportion_correctly():
    expected_query = '''
    WITH TotalSize AS (
        SELECT SUM(COALESCE(Size, 0)) AS totalSize
        FROM df
    )
    SELECT
        group_column,
        SUM(COALESCE(Size, 0)) / CAST(ts.totalSize AS DECIMAL) * 100 AS Proportion
    FROM
        df,
        TotalSize AS ts
    GROUP BY
        group_column, ts.totalSize;
    '''
    assert create_proportion_query("group_column") == expected_query


# Handles standard column names without special characters
def test_handles_standard_column_names():
    expected_query = '''
    WITH TotalSize AS (
        SELECT SUM(COALESCE(Size, 0)) AS totalSize
        FROM df
    )
    SELECT
        column_name,
        SUM(COALESCE(Size, 0)) / CAST(ts.totalSize AS DECIMAL) * 100 AS Proportion
    FROM
        df,
        TotalSize AS ts
    GROUP BY
        column_name, ts.totalSize;
    '''
    assert create_proportion_query("column_name") == expected_query


# Uses COALESCE to handle NULL values in Size column
def test_coalesce_handling():
    expected_query = '''
    WITH TotalSize AS (
        SELECT SUM(COALESCE(Size, 0)) AS totalSize
        FROM df
    )
    SELECT
        group_column,
        SUM(COALESCE(Size, 0)) / CAST(ts.totalSize AS DECIMAL) * 100 AS Proportion
    FROM
        df,
        TotalSize AS ts
    GROUP BY
        group_column, ts.totalSize;
    '''
    assert create_proportion_query('group_column') == expected_query


# Ensures the SQL query string is syntactically correct.
def test_sql_query_syntax():
    expected_query = '''
    WITH TotalSize AS (
        SELECT SUM(COALESCE(Size, 0)) AS totalSize
        FROM df
    )
    SELECT
        group_by_column,
        SUM(COALESCE(Size, 0)) / CAST(ts.totalSize AS DECIMAL) * 100 AS Proportion
    FROM
        df,
        TotalSize AS ts
    GROUP BY
        group_by_column, ts.totalSize;
    '''
    assert create_proportion_query("group_by_column") == expected_query