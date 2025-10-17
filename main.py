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
def run_for_articles(obsidian_note: ObsidianNote):
    if 'status' in obsidian_note.properties: return

    tags = obsidian_note.properties['tags']
    if "document/stub" in tags: 
        status = "stub"
        obsidian_note.properties['tags'].remove("document/stub")
    else:
        status = "complete"
    
    obsidian_note.insert_property_near_another("status", status, "tags", insert_after=False)

run_for_articles()