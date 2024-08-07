# %%
""" File from which to run the project (runs with f8) """

from helpers import ObsidianFile, doi_from_citation_key
import constants as c
from setup import yield_papers, split_links_property, add_missing_dois

for paper in yield_papers():
    paper: ObsidianFile
    title: str = paper.properties['title']
    title = title.lstrip('"').rstrip('"')
    title = f'"{title}"'

    paper.properties['title'] = title
    paper.update_flat_properties_from_properties_dict()
    paper.write_file()
    


# %% Test function
for file in yield_papers(limit=1):
    file: ObsidianFile