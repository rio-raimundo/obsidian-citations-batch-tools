# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""

from os.path import join
from helpers import ObsidianNote, process_articles, rename_articles
import constants as c

# Use the note renamer decorator

@rename_articles(limit=2, exclude_subfolders=False)
def rename_files(obsidian_note: ObsidianNote):
    if 'Mahowald' in obsidian_note.filename:
        old_name = obsidian_note.filename.rsplit(".md", 1)[0]
        new_name = old_name + '2'
        return old_name, new_name

# Call the function
rename_files()