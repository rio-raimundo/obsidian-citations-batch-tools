# %%
""" File from which to run the project (runs with f8) """

import constants as c
from setup import toggle_abstract_collapsing, update_zotero_links, update_DOIs_from_root_level_papers

update_DOIs_from_root_level_papers(c.vault_path)