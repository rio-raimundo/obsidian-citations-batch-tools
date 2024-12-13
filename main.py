# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""

from os.path import join
from helpers import ObsidianNote, process_articles, NoteRenamer
import constants as c

# Initialise file renamer
renamer = NoteRenamer()

@process_articles(limit=1, exclude_subfolders=False, write=False)
def files_to_rename(obsidian_note: ObsidianNote):
    old_name = obsidian_note.filename.rsplit(".md", 1)[0]
    new_name = old_name
    renamer.add(obsidian_note.filepath, old_name, new_name)

# Finally, call your function to execute it for the specified number of articles in a vault
files_to_rename()
renamer.rename_files()