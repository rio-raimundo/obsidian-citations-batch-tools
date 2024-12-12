# %%
#! %load_ext autoreload
#! %autoreload 3

""" File from which to run the project.

    Example usage: 

"""

# %%
from helpers import ObsidianNote, yield_articles, get_value_from_bibtex_entry, process_articles
import constants as c
from examples import move_tags_to_start

@process_articles(limit=-1, exclude_subfolders=False)
def test_decorator(obsidian_note: ObsidianNote):
    """ Move tags to the start of the file. """
    obsidian_note.insert_property_at_location('bobo', 'bozo', 0)

test_decorator()