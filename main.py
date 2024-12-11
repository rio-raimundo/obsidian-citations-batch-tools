# %%
""" File from which to run the project (runs with f8) """

from helpers import ObsidianFile, doi_from_citation_key
import constants as c
from setup import yield_articles, split_links_property, add_missing_dois, reorder_properties

#! %load_ext autoreload
#! %autoreload 3


# %% 

# Add archive tags to all papers
for article in yield_articles(limit=-1):
    article: ObsidianFile

    # Add archived tag as second tag, after 'first tag'
    tags: list = article.properties['tags']
    if 'archived' not in tags:
        tags = [tags.pop(0)] + ['archived'] + tags
        article.properties['tags'] = tags
    print(tags)

    article.update_flat_properties_from_properties_dict()
    article.write_file()

# %%
# Rename everything from paper to article

# Put 'first tags' as the first tag
for article in yield_articles(limit=-1):
    article: ObsidianFile

    tags: list = article.properties['tags']
    
    # Rename paper tag to article
    first_tags = ['article', 'book']
    for first_tag in first_tags:
        for idx, current_tag in enumerate(tags):

            if current_tag == first_tag:
                if idx != 0:
                    print(tags)
                    tags.pop(idx)
                    tags.insert(0, first_tag)

    article.update_flat_properties_from_properties_dict()
    article.write_file()


# %% 
# Try to import and read the bibtex file
from pybtex.database.input import bibtex

#open a bibtex file
parser = bibtex.Parser()
bibdata = parser.parse_file(c.bibtext_location)

# Find the publication journal in the object
def get_journal_from_citation_key(citation_key: str) -> str:
    if citation_key not in bibdata.entries: return None
    if 'journal' not in bibdata.entries[citation_key].fields: return None
    return bibdata.entries[citation_key].fields['journal']

# Loop through entries, get their journal entry, and add it as a property?
for article in yield_articles():
    article: ObsidianFile

    if article.properties.get('journal') is None:
        citation_key = article.properties['citation key']
        journal = get_journal_from_citation_key(citation_key)
        article.insert_property('journal', journal, 2)
    
    article.update_flat_properties_from_properties_dict()
    article.write_file()