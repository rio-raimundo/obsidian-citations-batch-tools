# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""

from os import rename
from pybtex.database import Person, Entry
from helpers import ObsidianNote, process_articles, rename_articles
import constants as c
import re

"""
This project currently contains two parent 'decorators' (the functions with the @ symbol) that can be used to modify ObsidianNote objects representing articles in a vault. These decorators are defined in the helpers/decorators.py file, and are imported here.

The two decorators are:
    - process_articles: This is the main decorator of this project. It takes in a user-defined function and runs it for each note in the vault.
    - rename_articles: This is a specialised decorator designed to enable the mass renaming of files. Its architecture needs to be separate from process_articles because it also goes through and updates all links to the renamed files. It also takes in a user-defined function, which must return the desired new name of the file.

Information on how to use both decorators is provided in the docstrings of the helpers/decorators.py file. Additionally, an extended example of how to use the process_articles decorator (the main decorator you will be using) is provided below. This example also includes an example of integrating with a BibTex file to pull extra information into your Obsidian notes.
"""
@process_articles(limit=1)
def add_year(obsidian_note: ObsidianNote):
    btex_data = obsidian_note.bibtex_data
    if (not hasattr(btex_data, 'fields') or 'date' not in btex_data.fields): return

    year = obsidian_note.bibtex_data.fields['date'].split('-')[0]
    obsidian_note.insert_property_near_another('year', year, 'authors', insert_after=False, override_existing=True)

# Finally, call your function to execute it for the specified number of articles in a vault
add_year()