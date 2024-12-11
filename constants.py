""" File for 'global' variables to be used across files. """
from os.path import join

# MANUALLY SET THESE VARIABLES
vault_path = r"C:\Users\rodrai\Desktop\github-repos\phd-vault"
excluded_folders = [r"\misc\zotero"]
relative_bibtex_location = r"misc\zotero\library.bib"

# AUTOMATIC SUPPORTING VARIABLES
bibtext_location = join(vault_path, relative_bibtex_location)