# %%
from pyzotero import zotero

api_key = "j0er33J84Skqas8G2Qsk1b0w"
library_id = 6101245
library_type = 'user'

zot = zotero.Zotero(library_id, library_type, api_key)
items = zot.top(limit=5)

# we've retrieved the latest five top-level items in our library
# we can print each item's item type and ID
for item in items:
    print('Item: %s | Key: %s' % (item['data']['itemType'], item['data']['key']))

# %%
