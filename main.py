# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""

from os.path import join
from helpers import ObsidianNote, process_articles

""" EXAMPLE USAGE OF THE CODE. """
# First call the decorator to process the articles, with arguments as needed (defaults used here)
# Then define your custom function and what it should do with each ObsidianNote (article) object
@process_articles(limit=-1, exclude_subfolders=False, write=False)
def add_custom_property(obsidian_note: ObsidianNote):
    """ Replace the filename of each article """
    filepath = obsidian_note.filepath
    folderpath, filename = filepath.rsplit('\\', 1)
    if ' & ' in filename:
        new_filename = filename.replace(' & ', ' and ')
        obsidian_note.replace_file(filepath=join(folderpath, new_filename))

# Finally, call your function to execute it for the specified number of articles in a vault
add_custom_property()