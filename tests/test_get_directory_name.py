import pytest

from hsr_size_analyzer.hsr_size_analyzer import get_directory_name


# Returns the first element when the list has one element
def test_returns_first_element_when_list_has_one_element():
    file_dir_list = ["dir1"]
    result = get_directory_name(file_dir_list)
    assert result == "dir1"


# Returns the second element when the list has two elements
def test_returns_second_element_with_two_elements():
    assert get_directory_name(["dir1", "dir2"]) == "dir2"


# Returns the second element when the list has more than two elements
def test_returns_second_element_when_list_has_more_than_two_elements():
    assert get_directory_name(["dir1", "dir2", "dir3"]) == "dir2"


# Handles an empty list without errors
def test_handles_empty_list():
    with pytest.raises(SystemExit):
        get_directory_name([])


# Handles a list with mixed data types
def test_handles_mixed_data_types():
    assert get_directory_name([1, 'folder', True]) == 'folder'


# Handles a list with non-string elements
def test_handles_non_string_elements():
    assert get_directory_name([1, "directory"]) == "directory"
