import pytest
import pandas as pd
from typing import Dict, List, Any

from hsr_size_analyzer.hsr_size_analyzer import create_dataframe


@pytest.fixture
def sample_file_data() -> Dict[str, List[Any]]:
    """Fixture to create a sample file_data dictionary."""
    return {
        'Extension': ['.txt', '.py', 'No extension', '.jpg'],
        'Size': [100, 500, 50, 1000],
        'Directory': ['docs', 'scripts', 'misc', 'images'],
        'Full Path': ['docs/file1.txt', 'scripts/script.py', 'misc/noext', 'images/photo.jpg']
    }


def test_create_dataframe(sample_file_data):
    """Test the create_dataframe function with sample data."""
    df = create_dataframe(sample_file_data)

    # Check if the result is a DataFrame
    assert isinstance(df, pd.DataFrame)

    # Check if the DataFrame has the correct columns
    expected_columns = ['Extension', 'Size', 'Directory', 'Full Path']
    assert list(df.columns) == expected_columns

    # Check if the DataFrame has the correct number of rows
    assert len(df) == len(sample_file_data['Extension'])

    # Check if the data in the DataFrame matches the input data
    for col in expected_columns:
        assert df[col].tolist() == sample_file_data[col]


def test_create_dataframe_empty_input():
    """Test create_dataframe with an empty dictionary."""
    empty_data = {
        'Extension': [],
        'Size': [],
        'Directory': [],
        'Full Path': []
    }
    df = create_dataframe(empty_data)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 0
    assert list(df.columns) == ['Extension', 'Size', 'Directory', 'Full Path']


def test_create_dataframe_missing_column():
    """Test create_dataframe with a missing column."""
    incomplete_data = {
        'Extension': ['.txt'],
        'Size': [100],
        'Directory': ['docs']
        # 'Full Path' is missing
    }
    df = create_dataframe(incomplete_data)

    # Check if the DataFrame was created
    assert isinstance(df, pd.DataFrame)

    # Check if all expected columns are present
    expected_columns = ['Extension', 'Size', 'Directory', 'Full Path']
    assert all(col in df.columns for col in expected_columns)

    # Check if the missing column is empty
    assert df['Full Path'].isnull().all()

    # Check if the other columns have the correct data
    assert df['Extension'].tolist() == ['.txt']
    assert df['Size'].tolist() == [100]
    assert df['Directory'].tolist() == ['docs']


def test_create_dataframe_extra_column():
    """Test create_dataframe with an extra column."""
    extra_data = {
        'Extension': ['.txt'],
        'Size': [100],
        'Directory': ['docs'],
        'Full Path': ['docs/file.txt'],
        'Extra': ['some_data']
    }
    df = create_dataframe(extra_data)

    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ['Extension', 'Size', 'Directory', 'Full Path']
    assert 'Extra' not in df.columns


def test_create_dataframe_column_order():
    """Test if create_dataframe maintains the specified column order."""
    unordered_data = {
        'Size': [100],
        'Full Path': ['docs/file.txt'],
        'Extension': ['.txt'],
        'Directory': ['docs']
    }
    df = create_dataframe(unordered_data)

    assert list(df.columns) == ['Extension', 'Size', 'Directory', 'Full Path']
