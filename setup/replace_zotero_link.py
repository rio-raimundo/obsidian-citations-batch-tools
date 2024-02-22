""" File to replace a zotero link with the new format. """
from helpers import ObsidianFile, yield_files
import constants as c

limit = -1  # -1 for default
idx = 0
for filepath in yield_files(c.vault_path, 'md'):
    if limit > 0 and idx >= limit: break

    file = ObsidianFile(filepath)
    if not file.property_contains_value('tags', 'paper'): continue

    # Find citation key and zotero link
    citation_key = file.return_property_values('citation key')[0]
    
    for link in file.return_property_values('links'):
        if 'zotero://select/' in link:
            zotero_link = link
            break
    
    new_zotero_link = f'zotero://select/items/@{citation_key}'
    file.replace_property_value(zotero_link, new_zotero_link)
    file.update_properties_in_contents()
    file.write_file(copy=False)
    idx += 1