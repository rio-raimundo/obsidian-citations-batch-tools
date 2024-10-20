# %%
""" File from which to run the project (runs with f8) """

from helpers import ObsidianFile, doi_from_citation_key
import constants as c
from setup import yield_articles, split_links_property, add_missing_dois, reorder_properties

# Add names as author tags

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



