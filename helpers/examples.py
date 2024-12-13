# %%
""" A list of some example functions which can be used with the yield_articles decorator to mass modify Obsidian article notes. """
from helpers import ObsidianNote, get_value_from_bibtex_entry
import constants as c

# %%
""" Add the 'journal' property and corresponding value to each article in the vault which does not currently have it. """

def add_journal_property_to_article(article: ObsidianNote):
    if article.properties.get('journal') is None:
        citation_key = article.properties['citation key']
        journal = get_value_from_bibtex_entry(citation_key, c.bibdata_entries, 'journal')
        article.insert_property_at_location('journal', journal, 2)

    elif article.properties['journal'] == '':
        citation_key = article.properties['citation key']
        journal = get_value_from_bibtex_entry(citation_key, c.bibdata_entries, 'journal')
        article.properties['journal'] = journal


# %% 
""" Move specific tags (e.g. 'document/article' to the start of the tags list). """

def move_tags_to_start(article: ObsidianNote, tags_to_move: list):
    """ Note that accessing the tags property directly will not modify flat properties, so you have to get a reference ot the properties themselves and update them at the end. """
    properties: dict = article.properties
    current_tags: list = properties['tags']
    
    # Rename paper tag to article
    for tag_to_move in tags_to_move:
        for idx, current_tag in enumerate(current_tags):

            if current_tag == tag_to_move:
                if idx != 0:
                    current_tags.pop(idx)
                    current_tags.insert(0, tag_to_move)

    article.properties = properties