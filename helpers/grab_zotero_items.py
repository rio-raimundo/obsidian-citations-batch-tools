# %%
from pyzotero import zotero

# Have to manually set, but shouldn't have to overwrite
api_key = "j0er33J84Skqas8G2Qsk1b0w"
library_id = 6101245
library_type = 'user'

zot = zotero.Zotero(library_id, library_type, api_key)
items = zot.top(limit=1)

# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
for item in items:
    print('Item: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))


""" 
- Mess around with seeing if you can get access to the journal name and updating all the files with them at some point.
"""

# %%
# Try to do this using the local bibtex tile
