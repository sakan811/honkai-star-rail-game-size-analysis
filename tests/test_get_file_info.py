import os
import tempfile
from typing import Tuple

import pytest

from hsr_size_analyzer.hsr_size_analyzer import get_file_info


@pytest.fixture
def temp_directory():
    """Create a temporary directory with a subdirectory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        subdir = os.path.join(tmpdir, 'subdir')
        os.makedirs(subdir)
        yield tmpdir


@pytest.fixture
def create_file(temp_directory):
    """Fixture to create a file in the temporary directory."""

    def _create_file(file_name: str, content: str, in_root: bool = False) -> str:
        if in_root or file_name.startswith('.'):
            file_path = os.path.join(temp_directory, file_name)
        else:
            file_path = os.path.join(temp_directory, 'subdir', file_name)
        with open(file_path, 'w') as f:
            f.write(content)
        return file_path

    return _create_file


@pytest.mark.parametrize("file_name, content, expected_ext, expected_dir, in_root", [
    ('file1.txt', 'Hello, World!', '.txt', 'subdir', False),
    ('file2.py', 'print("Python")', '.py', 'subdir', False),
    ('file3', 'No extension', '', 'subdir', False),
    ('.hidden_file', 'Hidden file', '', 'Root Directory', True),
    ('root_file.txt', 'Root file content', '.txt', 'Root Directory', True),
])
def test_get_file_info(temp_directory, create_file, file_name, content, expected_ext, expected_dir, in_root):
    """Test the get_file_info function with various file scenarios."""
    file_path = create_file(file_name, content, in_root)
    root = os.path.dirname(file_path)

    file_info = get_file_info(root, file_name, temp_directory)

    assert isinstance(file_info, Tuple)
    assert len(file_info) == 4

    file_ext, file_size, file_dir, full_file_path = file_info

    assert file_ext == expected_ext
    assert file_size == len(content)
    assert file_dir == expected_dir
    assert full_file_path == os.path.relpath(file_path, temp_directory)


def test_get_file_info_root_directory(temp_directory, create_file):
    """Test get_file_info for a file in the root directory."""
    root_file = 'root_file.txt'
    content = 'Root file content'
    create_file(root_file, content, in_root=True)

    root_file_info = get_file_info(temp_directory, root_file, temp_directory)

    assert root_file_info[2] == 'Root Directory'
    assert root_file_info[3] == root_file