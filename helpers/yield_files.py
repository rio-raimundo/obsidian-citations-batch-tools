""" Function to yield all files with a given extension within a given folder, including subfolders."""
import os
import fnmatch

def yield_files(folder_path: str, extension: str):
    """ Yield all files with a given extension within a given folder, including subfolders."""
    for root, dirs, files in os.walk(folder_path):
        for file_name in fnmatch.filter(files, f'*.{extension}'):
            file_path = os.path.join(root, file_name)
            yield file_path