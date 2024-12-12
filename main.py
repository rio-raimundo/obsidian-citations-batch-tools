# %%
#! %load_ext autoreload
#! %autoreload 3

""" File from which to run the project.

    Example usage:

    @process_articles(limit=20, exclude_subfolders=False)
    def YOUR_FUNCTION(obsidian_note: ObsidianNote):
        EXECUTE YOUR CODE HERE

    # call your function here
    test_decorator()

"""
from helpers import ObsidianNote, process_articles
import constants as c

@process_articles(limit=20, exclude_subfolders=False)
def test_decorator(obsidian_note: ObsidianNote):
    """ Move tags to the start of the file. """
    obsidian_note.insert_property_at_location('bobo', 'bozo', 0)

test_decorator()