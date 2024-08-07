# %%
""" File from which to run the project (runs with f8) """

from helpers import yield_papers, ObsidianFile
import constants as c
from setup import split_links_property

split_links_property(c.vault_path, copy_files=False, limit=-1)