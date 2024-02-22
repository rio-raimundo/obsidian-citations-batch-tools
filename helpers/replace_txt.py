# %%
""" File to replace a bit of text with another. """
import os
import fnmatch
import warnings

from execute_for_files import execute_for_files_in_folder

vault_path = r"C:\Users\hk23402\Desktop\Git_projects\mres-vault"

class ObsidianFile():
    """ Class to store data about a single obsidian file. """

    def __init__(self, filepath: str):
        self.filepath: str = filepath
        self.contents: list[str] = self.contents_list_from_filepath()

        # Properties
        self.property_idxs, self.flat_properties = self.create_flat_properties()
        self.properties = self.create_property_dict_from_flat_properties()

    def contents_list_from_filepath(self) -> list:
        """ Returns the contents of a file as a list."""
        with open(self.filepath, 'r', encoding='utf-8') as file:
            # Remove trailing newline
            return [line.rstrip('\n') for line in file.readlines()]
        
    def create_flat_properties(self) -> list:
        """ Returns idxs for start and end of properties, and list of flat properties. """
        empty = ((), ())
        contents = self.contents
        # Find idxs for first two instances of '---' line to identify properties
        if not contents or not contents[0].startswith("---"): return empty
        for line_idx in range(1, len(contents)):
            if contents[line_idx].startswith("---"): break
        else: 
            return empty  # return empty if no properties
        return (0, line_idx), contents[1: line_idx]
    
    def create_property_dict_from_flat_properties(self) -> dict:
        if not self.property_idxs: return {}  # return empty

        # Create grouped properties from flat property list
        property_dict: dict[str, list[str]] = {}
        current_key = ""
        for line in self.flat_properties:
            line: str

            # If 'key' line
            if line.endswith(':') or ': ' in line:
                key, spillover = line.split(':', 1)
                current_key = key.lower()
                property_dict[current_key] = []
                if spillover: property_dict[current_key].append(spillover[1:])
            # If 'value' line
            else:
                property_dict[current_key].append(line.lstrip('- '))
        return property_dict

    def property_contains_value(self, prop: str, value: str) -> bool:
        """ Identify if a given value is associated with a given value. """
        if not self.properties: return False
        prop, value = prop.lower(), value.lower()
        if prop not in self.properties: return False
        if value not in self.properties[prop]: return False
        return True
    
    def return_property_values(self, prop: str) -> list:
        """ Returns the values for a given tag. """
        return self.properties[prop.lower()]
    
    def replace_property_value(self, old_value: str, new_value: str):
        # Update flat properties
        for idx, line in enumerate(self.flat_properties):
            if old_value in line:
                self.flat_properties[idx] = line.replace(old_value, new_value)
                break

        # Recalculate properties dictionary
        self.properties = self.create_property_dict_from_flat_properties()
    
    def update_properties_in_contents(self):
        """ Function to update the properties in the contents using flat properties. """
        self.contents[self.property_idxs[0]+1: self.property_idxs[1]] = self.flat_properties

    def write_file(self, copy: bool = False):
        """ Write class contents to file. If copy is True, append '_copy' to the filename. """
        self.update_properties_in_contents()  # update contents before writing
        filepath = self.filepath.replace('.md', '_copy.md') if copy else self.filepath
        with open(filepath, 'w', encoding='utf-8') as file:
            file.writelines('\n'.join(self.contents))



def yield_files(folder_path: str, extension: str):
    """ Yield all files with a given extension within a given folder, including subfolders."""
    for root, dirs, files in os.walk(folder_path):
        for file_name in fnmatch.filter(files, f'*.{extension}'):
            file_path = os.path.join(root, file_name)
            yield file_path

limit = -1  # -1 for default
idx = 0
for filepath in yield_files(vault_path, 'md'):
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