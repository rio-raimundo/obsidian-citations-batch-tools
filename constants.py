""" Constnats file for 'global' variables to be used across files. Variables will be need to be set manually for each device, as it currently stands. """
from os.path import join
from pybtex.database.input import bibtex

# MANUALLY SET THESE VARIABLES
# Absoulte path to the vault
vault_path = r"C:\PATH\TO\OBSIDIAN\VAULT"

# List of folders where you don't want to search for articles (i.e. template folders). Comma separated. Relative to the root directory of your obsidian vault. 
excluded_folders = [r"\first\folder", r"\second\folder"]

# For some of the functionality, you will need to link to a .bib file, which can be generated automatically using the BetterBibtex plugin in Zotero, and the `export library -> Better BibLaTeX` format.
# ObsidianNotes can automatically get a reference to their BibLaTeX data, which can make operations easier. Currently, this is only implemented if articles have a property containing the BibTex citation key. If this is not the case for your vault, there are ways to find the correct BibTex entry by searching for e.g. the title of the article.
relative_bibtex_location = r"PATH\TO\BIBTEX\FILE\library.bib"
citation_key_property_name = "citation key"

# List of tags which will be used to identify articles. If a page contains one of these tags, it is treated as an article.
article_tags = ["document/article", "document/book"]

# AUTOMATIC SUPPORTING VARIABLES
# Load the bibtex file
bibtext_location = join(vault_path, relative_bibtex_location)
bibdata = bibtex.Parser().parse_file(bibtext_location)
bibdata_entries = bibdata.entries