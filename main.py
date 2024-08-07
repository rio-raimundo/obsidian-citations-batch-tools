# %%
""" File from which to run the project (runs with f8) """

from helpers import ObsidianFile
import constants as c
from setup import yield_papers, split_links_property

split_links_property(copy_files=False, limit=-1)

# %% Test function
for file in yield_papers(limit=1):
    file: ObsidianFile