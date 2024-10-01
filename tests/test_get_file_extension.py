from hsr_size_analyzer.hsr_size_analyzer import get_file_extension


def test_returns_correct_extension_for_standard_file():
    file_name = "example.txt"
    expected_extension = ".txt"
    assert get_file_extension(file_name) == expected_extension


# Returns correct extension for a file with no extension
def test_returns_correct_extension_for_file_with_no_extension():
    # Arrange
    file_name = "document"

    # Act
    result = get_file_extension(file_name)

    # Assert
    assert result == ""


# Returns correct extension for a file with a mixed-case extension
def test_returns_correct_extension_mixed_case():
    # Prepare
    file_name = "exampleFile.TXT"

    # Execute
    result = get_file_extension(file_name)

    # Assert
    assert result == ".txt"


# Returns correct extension for a file with multiple dots in the name
def test_returns_correct_extension_for_file_with_multiple_dots():
    # Prepare
    file_name = "example.file.name.txt"

    # Execute
    result = get_file_extension(file_name)

    # Assert
    assert result == ".txt"


# Handles files with unusual or rare extensions correctly
def test_handles_unusual_extensions():
    # Prepare
    file = "example_file.EXAMPLE"

    # Execute
    result = get_file_extension(file)

    # Assert
    assert result == ".example"


# Returns empty string for a file that starts with a dot and has no extension
def test_returns_empty_string_for_file_with_dot_no_extension():
    # Prepare
    file_name = ".htaccess"

    # Execute
    result = get_file_extension(file_name)

    # Assert
    assert result == ""


# Handles files with spaces in the name correctly
def test_handles_files_with_spaces():
    # Prepare
    file_name = "my file with spaces.txt"

    # Execute
    result = get_file_extension(file_name)

    # Assert
    assert result == ".txt"


# Handles files with special characters in the name correctly
def test_handles_special_characters():
    # Prepare
    file_name = "file_with_special!@#$%^&*()_+characters.txt"

    # Execute
    result = get_file_extension(file_name)

    # Assert
    assert result == ".txt"
