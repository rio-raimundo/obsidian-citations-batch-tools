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


def clean_abstract(s: str) -> str:
    # define characters to remove/replace
    invalid = r'[\\/:*?"<>|]'  # add others if needed
    s2 = re.sub(invalid, '', s)
    # also remove leading/trailing whitespace
    s2 = s2.strip()
    return f'"{s2}"'

# - Remove any tags starting with author names
@process_articles(limit=-1)
def remove_author_tags(obsidian_note: ObsidianNote):
    # Get reference to abstract and add to properties
    if 'abstract' not in obsidian_note.bibtex_data.fields: return
    abstract = obsidian_note.bibtex_data.fields['abstract']
    obsidian_note.properties['abstract'] = clean_abstract(abstract)

    # Update current abstract field with dataview
    found_abstract = False
    for idx, line in enumerate(obsidian_note.body_text):
        if line.startswith("> [!my-abstract]"):
            found_abstract = True
        elif found_abstract:
            if line.startswith("> "): obsidian_note.body_text[idx] = "> ` = this.abstract`"
            break


remove_author_tags()