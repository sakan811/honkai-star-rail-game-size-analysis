from typing import Dict, List, Any

import pytest

from hsr_size_analyzer.hsr_size_analyzer import append_file_info


@pytest.fixture
def empty_file_data() -> Dict[str, List[Any]]:
    """Fixture to create an empty file_data dictionary."""
    return {
        'Extension': [],
        'Size': [],
        'Directory': [],
        'Full Path': []
    }


def test_append_file_info(empty_file_data):
    """Test the append_file_info function with various file scenarios."""
    test_cases = [
        ('.txt', 100, 'documents', 'documents/file.txt'),
        ('.py', 500, 'scripts', 'scripts/script.py'),
        ('', 50, 'misc', 'misc/no_extension'),
        ('.hidden', 10, 'root', '.hidden_file'),
    ]

    for file_info in test_cases:
        append_file_info(empty_file_data, file_info)

    # Check if all lists have the same length
    assert len(set(map(len, empty_file_data.values()))) == 1

    # Check if the number of appended items matches the number of test cases
    assert len(empty_file_data['Extension']) == len(test_cases)

    # Check if the data was appended correctly
    for i, (ext, size, directory, full_path) in enumerate(test_cases):
        assert empty_file_data['Extension'][i] == (ext or 'No extension')
        assert empty_file_data['Size'][i] == size
        assert empty_file_data['Directory'][i] == directory
        assert empty_file_data['Full Path'][i] == full_path


def test_append_file_info_empty_extension(empty_file_data):
    """Test appending a file with no extension."""
    file_info = ('', 100, 'root', 'file_without_extension')
    append_file_info(empty_file_data, file_info)
    assert empty_file_data['Extension'][0] == 'No extension'


def test_append_file_info_multiple_calls(empty_file_data):
    """Test multiple calls to append_file_info."""
    file_info1 = ('.txt', 100, 'docs', 'docs/file1.txt')
    file_info2 = ('.py', 200, 'scripts', 'scripts/file2.py')

    append_file_info(empty_file_data, file_info1)
    append_file_info(empty_file_data, file_info2)

    assert len(empty_file_data['Extension']) == 2
    assert empty_file_data['Extension'] == ['.txt', '.py']
    assert empty_file_data['Size'] == [100, 200]
    assert empty_file_data['Directory'] == ['docs', 'scripts']
    assert empty_file_data['Full Path'] == ['docs/file1.txt', 'scripts/file2.py']


def test_append_file_info_empty_input(empty_file_data):
    """Test append_file_info with an empty tuple."""
    with pytest.raises(ValueError):
        append_file_info(empty_file_data, ())
