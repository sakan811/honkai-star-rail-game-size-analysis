import os
from typing import Any

import pandas as pd


def get_file_distribution(directory: str) -> pd.DataFrame:
    directory = normalize_directory_path(directory)

    # Ensure the directory ends with a forward slash
    directory = os.path.join(directory, '')

    # Dictionary to store total size and a set of directories for each extension
    file_data: dict[str, list[Any]] = {
        'Extension': [],
        'Size': [],
        'Directory': [],
        'Full Path': []
    }

    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_ext = get_file_extension(file)
            relative_path = os.path.relpath(root, directory)

            if relative_path == '.':
                file_dir = 'Root Directory'
            else:
                file_dir = relative_path

            full_file_path = os.path.relpath(file_path, directory)

            if file_ext == '':
                file_ext = 'No extension'

            file_size = os.path.getsize(file_path)  # Get file size

            file_data['Extension'].append(file_ext)
            file_data['Size'].append(file_size)
            file_data['Directory'].append(file_dir)
            file_data['Full Path'].append(full_file_path)

    # Create a DataFrame from the extension data
    df = pd.DataFrame(file_data, columns=['Extension', 'Size', 'Directory', 'Full Path'])

    return df


def get_directory_name(file_dir_list: list[str]) -> str:
    """
    Get the directory name based on the length of the directory list.
    If the length is 1, return the first element. If the length is 2 or more, return the second element.
    :param file_dir_list: List of directory elements.
    :return: The updated directory name.
    """
    if len(file_dir_list) == 1:
        return file_dir_list[0]
    elif len(file_dir_list) >= 2:
        return file_dir_list[1]
    else:
        raise SystemExit('The list of directory is empty.')


def get_file_extension(file: str) -> str:
    """
    Get the lowercase extension of a file.
    :param file: The file name.
    :return: The lowercase file extension.
    """
    return os.path.splitext(file)[-1].lower()


def normalize_directory_path(directory: str) -> str:
    """
    Normalize the directory path by replacing backslashes with forward slashes.
    If the directory contains double backslashes, they are also replaced with forward slashes.
    :param directory: The directory path to be normalized.
    :return: The normalized directory path.
    """
    return directory.replace('\\\\', '/').replace('\\', '/').replace('//', '/')