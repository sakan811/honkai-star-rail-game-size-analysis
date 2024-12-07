import os
import tempfile
from typing import Dict, List

import pytest

from hsr_size_analyzer.hsr_size_analyzer import collect_file_data


@pytest.fixture
def temp_directory():
    """Fixture to create a temporary directory with test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create directory structure
        os.makedirs(os.path.join(tmpdir, 'subdir1'))
        os.makedirs(os.path.join(tmpdir, 'subdir2'))

        # Create test files
        files = [
            (os.path.join(tmpdir, 'file1.txt'), 'Hello, World!'),
            (os.path.join(tmpdir, 'subdir1', 'file2.py'), 'print("Python")'),
            (os.path.join(tmpdir, 'subdir2', 'file3'), 'No extension'),
        ]
        for path, content in files:
            with open(path, 'w') as f:
                f.write(content)

        yield tmpdir


def test_collect_file_data_structure(temp_directory):
    """Test the structure of the collect_file_data result."""
    result = collect_file_data(temp_directory)

    assert isinstance(result, Dict)
    assert all(key in result for key in ['Extension', 'Size', 'Directory', 'Full Path'])
    assert all(isinstance(value, List) for value in result.values())
    assert len(result['Extension']) == 3  # We created 3 files


def test_collect_file_data_extensions(temp_directory):
    """Test the file extensions in the collect_file_data result."""
    result = collect_file_data(temp_directory)

    assert '.txt' in result['Extension']
    assert '.py' in result['Extension']
    assert 'No extension' in result['Extension']


def test_collect_file_data_sizes(temp_directory):
    """Test the file sizes in the collect_file_data result."""
    result = collect_file_data(temp_directory)

    assert 13 in result['Size']  # Size of 'Hello, World!'
    assert 15 in result['Size']  # Size of 'print("Python")'
    assert 12 in result['Size']  # Size of 'No extension'


def test_collect_file_data_directories(temp_directory):
    """Test the directories in the collect_file_data result."""
    result = collect_file_data(temp_directory)

    assert 'Root Directory' in result['Directory']
    assert 'subdir1' in result['Directory']
    assert 'subdir2' in result['Directory']


def test_collect_file_data_paths(temp_directory):
    """Test the file paths in the collect_file_data result."""
    result = collect_file_data(temp_directory)

    assert 'file1.txt' in result['Full Path']
    assert os.path.join('subdir1', 'file2.py') in result['Full Path']
    assert os.path.join('subdir2', 'file3') in result['Full Path']