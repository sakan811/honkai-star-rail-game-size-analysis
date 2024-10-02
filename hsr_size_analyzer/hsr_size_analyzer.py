import os
from typing import Any

import pandas as pd


def get_file_distribution(directory: str) -> pd.DataFrame:
    directory = normalize_directory_path(directory)
    directory = os.path.abspath(directory)

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
            file_dir = 'Root Directory' if relative_path == '.' else relative_path
            full_file_path = os.path.relpath(file_path, directory)
            file_size = os.path.getsize(file_path)
            
            file_data['Extension'].append(file_ext or 'No extension')
            file_data['Size'].append(file_size)
            file_data['Directory'].append(file_dir)
            file_data['Full Path'].append(full_file_path)

    # Create a DataFrame from the extension data
    df = pd.DataFrame(file_data, columns=['Extension', 'Size', 'Directory', 'Full Path'])

    return df


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
    if not directory:
        return ""
    
    # First, replace all backslashes with forward slashes
    normalized = directory.replace('\\', '/')
    
    # Then, collapse multiple consecutive slashes into a single slash
    while '//' in normalized:
        normalized = normalized.replace('//', '/')
    
    return normalized
