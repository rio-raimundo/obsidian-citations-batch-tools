""" Constnats file for 'global' variables to be used across files. Variables will be need to be set manually for each device, as it currently stands. """
from os.path import join
from pybtex.database.input import bibtex

# MANUALLY SET THESE VARIABLES
# Absoulte path to the vault
vault_path = r"C:\Users\rodrai\Desktop\github-repos\phd-vault"

# List of folders where you don't want to search for articles (i.e. template folders)
excluded_folders = [r"\misc\zotero"]

# For some of the functionality, you will need to link to a .bib file, which can be generated automatically using the BetterBibtex plugin in Zotero.
relative_bibtex_location = r"misc\zotero\library.bib"

# List of tags which will be used to identify articles. If a page contains one of these tags, it is treated as an article.
article_tags = ["document/article", "document/book"]

# AUTOMATIC SUPPORTING VARIABLES
# Load the bibtex file
bibtext_location = join(vault_path, relative_bibtex_location)
bibdata = bibtex.Parser().parse_file(bibtext_location)
bibdata_entries = bibdata.entries