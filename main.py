# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""

from helpers import ObsidianNote, process_articles, rename_articles
import constants as c

"""
This project currently contains two parent 'decorators' (the functions with the @ symbol) that can be used to modify ObsidianNote objects representing articles in a vault. These decorators are defined in the helpers/decorators.py file, and are imported here.

The two decorators are:
    - process_articles: This is the main decorator of this project. It takes in a user-defined function and runs it for each note in the vault.
    - rename_articles: This is a specialised decorator designed to enable the mass renaming of files. Its architecture needs to be separate from process_articles because it also goes through and updates all links to the renamed files. It also takes in a user-defined function, which must return the desired new name of the file.

Information on how to use both decorators is provided in the docstrings of the helpers/decorators.py file. Additionally, an extended example of how to use the process_articles decorator (the main decorator you will be using) is provided below. This example also includes an example of integrating with a BibTex file to pull extra information into your Obsidian notes.
"""
@process_articles(limit=-1, exclude_subfolders=False, write=True)
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

# Finally, call your function to execute it for the specified number of articles in a vault
update_journals()