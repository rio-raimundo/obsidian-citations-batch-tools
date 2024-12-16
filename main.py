# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""

from os.path import join
from helpers import ObsidianNote, process_articles, rename_articles
import constants as c

# Use the note renamer decorator

@rename_articles(limit=2)
def rename_files(obsidian_note: ObsidianNote):
    if 'Mahowald' in obsidian_note.filename:
        new_name = obsidian_note.filename.rsplit(".md", 1)[0] + '2' + '.md'
        return new_name

# Call the function
rename_files()