# %%
""" THIS WORKS BUT YOU CAN'T COPY PASTE IT INTO ZOTERO SEARCH BECAUSE THERE IS NO 'OR' OPERATOR. """

import os
import glob
        
def autogen_citation_keys(folder_path: str):
    # List all .md files in the folder
    file_list = [os.path.basename(file) for file in glob.glob(f"{folder_path}/*.md")]

    # Remove those with brackets (to filter new format files), and remove '.md'
    file_list = [file[:-3] for file in file_list if '(' not in file]

    # Convert to format that can be copy pasted into zotero integration
    file_string = ", ".join(file_list)

# use right click -> copy path -> add 'r' in front
folder_path = r"C:\Users\hk23402\Desktop\Git_projects\mres-vault\__General\Computational cognition\Papers"
citation_keys = autogen_citation_keys(folder_path)
print(citation_keys)