# %%
""" File from which to run the project (runs with f8) """

from helpers import ObsidianNote
import constants as c

#! %load_ext autoreload
#! %autoreload 3

# %% 
# Add archive tags to all papers
for article in yield_articles(limit=-1):
    article: ObsidianNote

    # Add archived tag as second tag, after 'first tag'
    tags: list = article.properties_dict['tags']
    if 'archived' not in tags:
        tags = [tags.pop(0)] + ['archived'] + tags
        article.properties_dict['tags'] = tags
    print(tags)

    article._flat_properties_from_dict()
    article.write_file()

# %%
# Rename everything from paper to article

# Put 'first tags' as the first tag
for article in yield_articles(limit=-1):
    article: ObsidianNote

    tags: list = article.properties_dict['tags']
    
    # Rename paper tag to article
    first_tags = ['article', 'book']
    for first_tag in first_tags:
        for idx, current_tag in enumerate(tags):

            if current_tag == first_tag:
                if idx != 0:
                    print(tags)
                    tags.pop(idx)
                    tags.insert(0, first_tag)

    article._flat_properties_from_dict()
    article.write_file()


# %% 
# Try to import and read the bibtex file


# Find the publication journal in the object
def get_journal_from_citation_key(citation_key: str) -> str:
    if citation_key not in c.bibdata.entries: return None
    if 'journal' not in c.bibdata.entries[citation_key].fields: return None
    return c.bibdata.entries[citation_key].fields['journal']

# Loop through entries, get their journal entry, and add it as a property?
for article in yield_articles():
    article: ObsidianNote

    if article.properties_dict.get('journal') is None:
        citation_key = article.properties_dict['citation key']
        journal = get_journal_from_citation_key(citation_key)
        article.insert_property_at_location('journal', journal, 2)
    
    article._flat_properties_from_dict()
    article.write_file()


# %%
# Move the journal property to the top of the properties
for article in yield_articles(limit=-1):
    article: ObsidianNote

    if article.properties_dict.get('journal') is not None:
        journal = article.properties_dict.pop('journal')
        article.insert_property_at_location('journal', journal, 1)
    
    article._flat_properties_from_dict()
    article.write_file()