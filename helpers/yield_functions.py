""" Function to yield all files with a given extension within a given folder, including subfolders."""

import os
import fnmatch

from helpers import ObsidianFile

def yield_files(folder_path: str, extension: str, exclude_subfolders: bool = False):
    """ Yield all files with a given extension within a given folder."""
    # Assign single root directory and list of files manually if excluding subfolders else calc with os.walk
    if exclude_subfolders: directories = [(folder_path, os.listdir(folder_path))]
    else: directories = [(root, files) for root, _, files in os.walk(folder_path)]

    # Iterate through each root and set of files in directory and yield files with given extension
    for root, files in directories:
        for file_name in fnmatch.filter(files, f'*.{extension}'):
            file_path = os.path.join(root, file_name)
            yield file_path

def yield_papers(vault_path: str, limit: int = -1, exclude_subfolders: bool = False):
    """ Yields each paper in a vault as ObsidianFile object. """
    idx = 0
    for filepath in yield_files(vault_path, 'md', exclude_subfolders):
        if limit > 0 and idx >= limit: break

        file = ObsidianFile(filepath)
        if not file.property_contains_value('tags', 'paper'): continue
        idx += 1
        yield file