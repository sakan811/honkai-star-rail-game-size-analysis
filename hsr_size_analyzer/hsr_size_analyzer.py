import os
from typing import Any, Dict, List, Tuple

import pandas as pd


def get_file_distribution(directory: str) -> pd.DataFrame:
    """
    Generate a DataFrame containing file distribution information for a given directory.
    :param directory: The path to the directory to analyze.
                    This can be either an absolute path or relative path.
    :return: Pandas DataFrame containing file distribution information.
    """
    directory = normalize_directory_path(directory)
    directory = os.path.abspath(directory)

    file_data = collect_file_data(directory)
    return create_dataframe(file_data)


def collect_file_data(directory: str) -> Dict[str, List[Any]]:
    """
    Collect file data from the given directory and its subdirectories.
    :param directory: Path to the directory to analyze
    :return: Dictionary containing lists of file information
    """
    file_data: Dict[str, List[Any]] = {
        'Extension': [],
        'Size': [],
        'Directory': [],
        'Full Path': []
    }

    for root, _, files in os.walk(directory):
        for file in files:
            file_info = get_file_info(root, file, directory)
            append_file_info(file_data, file_info)

    return file_data


def get_file_info(root: str, file: str, base_directory: str) -> Tuple[str, int, str, str]:
    """
    Gather information about a specific file.
    :param root: The root directory of the file
    :param file: The name of the file
    :param base_directory: The base directory for relative path calculations
    :return: Tuple containing file extension, size, directory, and full path
    """
    file_path = os.path.join(root, file)
    file_ext = get_file_extension(file)
    relative_path = os.path.relpath(root, base_directory)
    file_dir = 'Root Directory' if relative_path == '.' else relative_path
    full_file_path = os.path.relpath(file_path, base_directory)
    file_size = os.path.getsize(file_path)

    return file_ext, file_size, file_dir, full_file_path


def append_file_info(file_data: Dict[str, List[Any]], file_info: Tuple[str, int, str, str]) -> None:
    """
    Append file information to the file_data dictionary.
    :param file_data: Dictionary containing lists of file information
    :param file_info: Tuple containing information about a single file
    :return: None
    """
    file_ext, file_size, file_dir, full_file_path = file_info
    file_data['Extension'].append(file_ext or 'No extension')
    file_data['Size'].append(file_size)
    file_data['Directory'].append(file_dir)
    file_data['Full Path'].append(full_file_path)


def create_dataframe(file_data: Dict[str, List[Any]]) -> pd.DataFrame:
    """
    Create a pandas DataFrame from the collected file data.
    :param file_data: Dictionary containing lists of file information
    :return: DataFrame with columns for Extension, Size, Directory, and Full Path
    """
    return pd.DataFrame(file_data, columns=['Extension', 'Size', 'Directory', 'Full Path'])


def get_file_extension(file: str) -> str:
    """
    Get the lowercase extension of a file.
    :param file: The file name.
    :return: The lowercase file extension.
    """
    return os.path.splitext(file)[-1].lower()


def normalize_directory_path(directory: str) -> str:
    """
    Normalize the directory path by replacing backslashes with forward slashes,
    collapsing multiple consecutive slashes, and preserving trailing slashes.

    :param directory: The directory path to be normalized.
    :return: The normalized directory path.
    """
    if not directory:
        return ""

    # Replace backslashes with forward slashes
    normalized = directory.replace('\\', '/')

    # Collapse multiple slashes, but preserve leading double slash for UNC paths
    if normalized.startswith('//'):
        normalized = '/' + normalized.lstrip('/')
    normalized = os.path.normpath(normalized)

    # Replace backslashes again (normpath may have added some)
    normalized = normalized.replace('\\', '/')

    # Preserve the trailing slash if it was in the original path
    if directory.endswith('/') or directory.endswith('\\'):
        normalized += '/'

    return normalized
