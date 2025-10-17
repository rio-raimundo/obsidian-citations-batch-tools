# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""

import re
from collections import defaultdict
from os import rename

from pybtex.database import Entry, Person

import constants as c
from helpers import ObsidianNote, process_articles, rename_articles


# --- HELPER FUNCTIONS ---
def format_author(name: Person) -> str:
    return f"{name.first_names[0][0]}.{''.join(name.last_names)}".lower()

# - MAIN PROCESS FUNCTION TO POPULATE AUTHORS DICT --- 
@process_articles(limit=-1)
def find_similar_authors(obsidian_note: ObsidianNote):
    # Get our authors from the bibtex data as a list of Persons
    btex_data: Entry = obsidian_note.bibtex_data
    if 'author' not in btex_data.persons: return
    authors: list[Person] = btex_data.persons['author']