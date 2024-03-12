""" Function to yield all files with a given extension within a given folder, including subfolders."""

import os
import fnmatch

from helpers import ObsidianFile

def yield_files(folder_path: str, extension: str):
    """ Yield all files with a given extension within a given folder, including subfolders."""
    for root, dirs, files in os.walk(folder_path):
        for file_name in fnmatch.filter(files, f'*.{extension}'):
            file_path = os.path.join(root, file_name)
            yield file_path

def yield_papers(vault_path: str, limit: int =-1):
    """ Yields each paper in a vault as ObsidianFile object. """
    idx = 0
    for filepath in yield_files(vault_path, 'md'):
        if limit > 0 and idx >= limit: break

        file = ObsidianFile(filepath)
        if not file.property_contains_value('tags', 'paper'): continue
        yield file