""" File for 'global' variables to be used across files. """
from os.path import join

# MANUALLY SET THESE VARIABLES
# Absoulte path to the vault
vault_path = r"C:\Users\rodrai\Desktop\github-repos\phd-vault"

# List of folders where you don't want to search for articles (i.e. template folders)
excluded_folders = [r"\misc\zotero"]

# For some of the functionality, you will need to link to a .bib file, which can be generated automatically using the BetterBibtex plugin in Zotero.
relative_bibtex_location = r"misc\zotero\library.bib"


# AUTOMATIC SUPPORTING VARIABLES
bibtext_location = join(vault_path, relative_bibtex_location)