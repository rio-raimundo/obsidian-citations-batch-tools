""" Function to yield all files with a given extension within a given folder, including subfolders."""

import os
import fnmatch

from helpers import ObsidianNote
import constants as c

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

def yield_notes(limit: int = -1, exclude_subfolders: bool = False):
    """ Yields each note in a vault as ObsidianNote object. """
    # Check if folder exists
    if not os.path.exists(c.vault_path):
        raise FileNotFoundError(f"Folder {c.vault_path} does not exist.")

    idx = 0
    for filepath in yield_files(c.vault_path, 'md', exclude_subfolders):
        
        # Ignore files in excluded folders
        should_continue = False
        for excluded_folder in c.excluded_folders:
            folderpath = os.path.join(c.vault_path, excluded_folder)
            if filepath.startswith(folderpath):
                should_continue = True
                break
        if should_continue: continue

        # Limit number of files
        if limit > 0 and idx >= limit: break
        idx += 1

        obsidian_note: ObsidianNote = ObsidianNote(filepath)
        yield obsidian_note

def yield_articles(limit: int = -1, exclude_subfolders: bool = False):
    """ Yields only articles in a vault as ObsidianNote objects. """

    idx = 0
    for obsidian_note in yield_notes(-1, exclude_subfolders):
        if not any([obsidian_note.property_contains_value('tags', tag) for tag in c.article_tags]): continue

        # Limit number of files
        if limit > 0 and idx >= limit: break
        idx += 1

        yield obsidian_note