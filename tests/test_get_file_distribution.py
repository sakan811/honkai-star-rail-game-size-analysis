from unittest.mock import patch

import pandas as pd
import pytest

from hsr_size_analyzer.hsr_size_analyzer import get_file_distribution, normalize_directory_path


@pytest.fixture
def mock_walk():
    return [
        ('/root', [], ['file1.txt', 'file2.py', 'file3']),
        ('/root/subdir', [], ['file4.jpg', 'file5.txt']),
    ]

@pytest.fixture
def mock_getsize():
    return {
        '/root/file1.txt': 100,
        '/root/file2.py': 200,
        '/root/file3': 150,
        '/root/subdir/file4.jpg': 300,
        '/root/subdir/file5.txt': 250,
    }

@patch('os.walk')
@patch('os.path.getsize')
@patch('os.path.join', lambda *args: '/'.join(args))
def test_get_file_distribution(mock_getsize, mock_walk):
    mock_walk.return_value = [
        ('/root', [], ['file1.txt', 'file2.py', 'file3']),
        ('/root/subdir', [], ['file4.jpg', 'file5.txt']),
    ]
    mock_getsize.side_effect = lambda x: {
        '/root/file1.txt': 100,
        '/root/file2.py': 200,
        '/root/file3': 150,
        '/root/subdir/file4.jpg': 300,
        '/root/subdir/file5.txt': 250,
    }.get(x, 0)

    result = get_file_distribution('/root')

    expected_data = {
        'Extension': ['.txt', '.py', 'No extension', '.jpg', '.txt'],
        'Size': [100, 200, 150, 300, 250],
        'Directory': ['Root Directory', 'Root Directory', 'Root Directory', 'subdir', 'subdir'],
        'Full Path': ['file1.txt', 'file2.py', 'file3', 'subdir/file4.jpg', 'subdir/file5.txt']
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result, expected_df)

def test_normalize_directory_path():
    assert normalize_directory_path('C:\\Users\\test') == 'C:/Users/test'
    assert normalize_directory_path('C:\\\\Users\\\\test') == 'C:/Users/test'
    assert normalize_directory_path('/home/user//test') == '/home/user/test'
    assert normalize_directory_path('/home/user/test/') == '/home/user/test/'

@patch('os.walk')
@patch('os.path.getsize')
@patch('os.path.join', lambda *args: '/'.join(args))
def test_empty_directory(mock_getsize, mock_walk):
    mock_walk.return_value = []
    mock_getsize.return_value = 0

    result = get_file_distribution('/empty')

    expected_df = pd.DataFrame({
        'Extension': [],
        'Size': [],
        'Directory': [],
        'Full Path': []
    })

    pd.testing.assert_frame_equal(result, expected_df)

@patch('os.walk')
@patch('os.path.getsize')
@patch('os.path.join', lambda *args: '/'.join(args))
def test_directory_with_only_subdirectories(mock_getsize, mock_walk):
    mock_walk.return_value = [
        ('/root', ['subdir1', 'subdir2'], []),
        ('/root/subdir1', [], []),
        ('/root/subdir2', [], []),
    ]
    mock_getsize.return_value = 0

    result = get_file_distribution('/root')

    expected_df = pd.DataFrame({
        'Extension': [],
        'Size': [],
        'Directory': [],
        'Full Path': []
    })

    pd.testing.assert_frame_equal(result, expected_df)

@patch('os.walk')
@patch('os.path.getsize')
@patch('os.path.join', lambda *args: '/'.join(args))
def test_directory_with_hidden_files(mock_getsize, mock_walk):
    mock_walk.return_value = [
        ('/root', [], ['.hidden1', '.hidden2', 'visible.txt']),
    ]
    mock_getsize.side_effect = lambda x: 100 if 'visible' in x else 50

    result = get_file_distribution('/root')

    expected_data = {
        'Extension': ['No extension', 'No extension', '.txt'],
        'Size': [50, 50, 100],
        'Directory': ['Root Directory', 'Root Directory', 'Root Directory'],
        'Full Path': ['.hidden1', '.hidden2', 'visible.txt']
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result, expected_df)

@patch('os.walk')
@patch('os.path.getsize')
@patch('os.path.join', lambda *args: '/'.join(args))
def test_directory_with_large_files(mock_getsize, mock_walk):
    mock_walk.return_value = [
        ('/root', [], ['large1.bin', 'large2.bin']),
    ]
    mock_getsize.side_effect = lambda x: 1024 * 1024 * 1024 if 'large1' in x else 2 * 1024 * 1024 * 1024

    result = get_file_distribution('/root')

    expected_data = {
        'Extension': ['.bin', '.bin'],
        'Size': [1024 * 1024 * 1024, 2 * 1024 * 1024 * 1024],
        'Directory': ['Root Directory', 'Root Directory'],
        'Full Path': ['large1.bin', 'large2.bin']
    }
    expected_df = pd.DataFrame(expected_data)

    pd.testing.assert_frame_equal(result, expected_df)