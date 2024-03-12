# %%
""" File from which to run the project (runs with f8) """

import constants as c
from setup import toggle_abstract_collapsing, update_zotero_links

toggle_abstract_collapsing(c.vault_path, become_open=False, limit=1, copy_files=True)

