# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""

from os.path import join
from helpers import ObsidianNote, process_articles
import constants as c

<<<<<<< HEAD
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
=======
""" EXAMPLE USAGE OF THE CODE. The general process is as follows: 
    - First, call the decorator `process_articles` with the desired arguments. This will process the articles in the vault and make them available to the function you define.
    - Define a function that takes an `ObsidianNote` object as an argument. This function will be executed on each article in the vault.
"""
@process_articles(limit=20, exclude_subfolders=False, write=True)
def update_journals(obsidian_note: ObsidianNote):
    """ EXAMPLE FUNCTION.
        - Updates the 'journal' property of an ObsidianNote object, or adds it if it does not have it.
        - Also moves it to a specificied location in the properties list (specified in initial variable).
    """
    location = 2

    # Delete current reference to property if it already exists
    # NOTE: we could check if this is in the right place, but read/write operations are so fast this is fine
    if 'journal' in obsidian_note.properties:
        del obsidian_note.properties['journal']
    
    # Add in the journal property into the specified location
    # NOTE: this call relies on obsidian_note.bibtex_data(), which reads the BibTex data using the `c.bibtex_path` constant, and assumes that the ObsidianNote has a property 'citation key' that contains the BibTex citation key. The name of this property can be specified in the constants file.

    # Returns the value of the 'journal' key in the BibTex data, or None if it does not exist
    journal = obsidian_note.bibtex_data.get('journal', None)

    # Insert the property at a specified location
    obsidian_note.insert_property_at_location('journal', journal, location)
>>>>>>> 596f2bb... * Updated example function to use the BibTex data, to make it easier to understand how this works!

# Finally, call your function to execute it for the specified number of articles in a vault
update_journals()