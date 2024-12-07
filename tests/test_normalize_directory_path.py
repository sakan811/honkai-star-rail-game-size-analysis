from hsr_size_analyzer.hsr_size_analyzer import normalize_directory_path


def test_converts_single_backslashes_to_forward_slashes():
    # Given
    input_path = "C:\\Users\\Test"
    expected_output = "C:/Users/Test"

    # When
    result = normalize_directory_path(input_path)

    # Then
    assert result == expected_output


def test_handles_empty_string_input():
    # Given
    input_path = ""
    expected_output = ""

    # When
    result = normalize_directory_path(input_path)

    # Then
    assert result == expected_output


# Returns the same path if no backslashes are present
def test_returns_same_path_if_no_backslashes_present():
    # Given
    input_path = "C:/Users/Test"
    expected_output = "C:/Users/Test"

    # When
    result = normalize_directory_path(input_path)

    # Then
    assert result == expected_output


# Converts double backslashes to forward slashes
def test_converts_double_backslashes_to_forward_slashes():
    # Given
    input_path = "C:\\\\Users\\\\Test"
    expected_output = "C:/Users/Test"

    # When
    result = normalize_directory_path(input_path)

    # Then
    assert result == expected_output


# Handles paths with only forward slashes
def test_handles_paths_with_only_forward_slashes():
    # Given
    directory_path = "C:/Users/Documents"

    # When
    normalized_path = normalize_directory_path(directory_path)

    # Then
    assert normalized_path == "C:/Users/Documents"


# Handles paths with multiple consecutive backslashes
def test_handles_multiple_consecutive_backslashes():
    # Given
    directory_path = 'C:\\\\Users\\\\John\\\\Documents'

    # When
    normalized_path = normalize_directory_path(directory_path)

    # Then
    assert normalized_path == 'C:/Users/John/Documents'


# Handles paths with mixed slashes (both backslashes and forward slashes)
def test_handles_mixed_slashes():
    # Given
    mixed_slash_path = 'C:\\Users\\Documents//Project\\Files'

    # When
    normalized_path = normalize_directory_path(mixed_slash_path)

    # Then
    assert normalized_path == 'C:/Users/Documents/Project/Files'


def test_normalize_directory_path_with_trailing_slashes():
    test_cases = [
        ('C:\\Users\\test\\', 'C:/Users/test/'),
        ('C:\\\\Users\\\\test\\\\', 'C:/Users/test/'),
        ('/home/user//test//', '/home/user/test/'),
        ('//home//user//test//', '/home/user/test/'),
    ]

    for input_path, expected_output in test_cases:
        assert normalize_directory_path(input_path) == expected_output, \
            f"Failed for input: {input_path}"