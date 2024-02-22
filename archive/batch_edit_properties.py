# %%

# 1. Find all 'papers' by searching for the 'papers' tag.
# 2. Separate tags using ':' syntax. 

import warnings

from execute_for_files import execute_for_files_in_folder

vault_path = r"C:\Users\hk23402\Desktop\Git_projects\mres-vault"
        
def get_properties_from_content(file_path: list):
    """ Read file from a file path and group them into a list of lists, where each item in outer list corresponds to a property."""
    def return_properties(content: str):
        status = 0
        trimmed_content = []
        idxs = []
        for idx, line in enumerate(content):
            if status == 2: return trimmed_content, idxs
            if "---" in line:
                status += 1
                idxs.append(idx)
            elif status == 1: trimmed_content.append(line)
        return trimmed_content, idxs
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = [line.strip() for line in file.readlines()]

    flat_properties, idxs = return_properties(content)
    if flat_properties == []: return [], [], [], []  # return empty if not paper

    # Create grouped properties using sublists
    grouped_properties = []
    for line in flat_properties:
        if ':' in line and not line.startswith('- '): grouped_properties.append([line])
        else: grouped_properties[-1].append(line)
    
    # Check if paper tag exists; if not, return empty
    is_paper = False
    for property in grouped_properties:
        if 'tags:' in property[0].lower():
            # Replace if upper case
            if 'tags' in property[0]: property[0] = property[0].replace('tags', 'Tags')
            for line in property:
                if 'paper' in line: is_paper = True
    if not is_paper: return [], [], [], []
    
    # Store tuple of property names
    property_names = [line[0].split(':')[0] for line in grouped_properties]
    return grouped_properties, property_names, content, idxs

def reorder_properties(file_path: list, order: list[str]):
    grouped_properties, property_names, content, idxs = get_properties_from_content(file_path)
    if grouped_properties == []: return

    # Sort grouped_properties using custom lambda function
    def sort_by_keyword(x):
        keyword = x[0].split(':')[0]
        return order.index(keyword)
    sorted_properties = sorted(grouped_properties, key=lambda x: sort_by_keyword(x))

    # Flatten 2d list into list
    sorted_properties = [item for sublist in sorted_properties for item in sublist]
    new_idxs = [idxs[0]+1, idxs[1]]  # ignore idxs of '---' lines

    content[new_idxs[0]:new_idxs[1]] = sorted_properties

    with open(file_path, 'w', encoding='utf-8') as file:
        file.writelines('\n'.join(content))


def main(order: str = None):
    # Get all unique property names in papers in vault
    all_property_names = set()
    for _, property_names, _, _ in execute_for_files_in_folder(vault_path, 'md', get_properties_from_content):
        all_property_names.update(property_names)
    
    # If order not given, just return as a list
    if order is None: return list(all_property_names)

    # If order given, first check it matches
    if set(order) != set(all_property_names):
        warnings.warn(f"Order does not match! Returning all properties")
        return all_property_names
    
    # If matches, reorder
    for _ in execute_for_files_in_folder(vault_path, 'md', reorder_properties, order):
        pass
        

order = [
    'Title',
    'Tags',
    'Citation Key',
    'Authors',
    'Links',
    'Status',
    'aliases',
    'sr-due',
    'sr-interval',
    'sr-ease',
    ]
a = main(order)