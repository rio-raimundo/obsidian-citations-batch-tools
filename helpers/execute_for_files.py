import os
import fnmatch

def execute_for_files_in_folder(folder_path: str, extension: str, func: object, *args):
    """ 
    Execute a function for all files with a given extension within a given folder, including subfolders. Yields one value at a time.
    """
    for root, dirs, files in os.walk(folder_path):
        for file_name in fnmatch.filter(files, f'*.{extension}'):
            file_path = os.path.join(root, file_name)
            yield func(file_path, *args)