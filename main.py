# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""

from helpers import ObsidianNote, process_articles

""" EXAMPLE USAGE OF THE CODE. """
# First call the decorator to process the articles, with arguments as needed (defaults used here)
# Then define your custom function and what it should do with each ObsidianNote (article) object
@process_articles(limit=-1, exclude_subfolders=False, make_copies=False)
def add_custom_property(obsidian_note: ObsidianNote):
    """ Example function that adds the custom property 'modified' to the end of each note. """
    obsidian_note.insert_property_at_location('modified', 'Yes', location=-1)

# Finally, call your function to execute it for the specified number of articles in a vault
add_custom_property()