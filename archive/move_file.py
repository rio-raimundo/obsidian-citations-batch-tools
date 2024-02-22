# %%
""" Script to move a file and all attachments from one vault to another. """
import re
import os
import shutil

from execute_for_files import execute_for_files_in_folder

def copy_file(file_name: str, vault_from: str, vault_to: str, attachments_to: str = "", attachments_from: str = ""):
    """ Copy a file from one vault to another. """
    def match_file(file_path: str, target_file_name: str):
        """ Match a file path to a target file name. Return content of that file if matched. Else return None. """
        current_file_name = file_path.split("\\")[-1].split(".")[0]
        if target_file_name == current_file_name:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = [line.strip() for line in file.readlines()]
            return content, file_path
        return None, None

    # Return the content of a specific file, if exists
    for content, file_path in execute_for_files_in_folder(vault_from, "md", match_file, file_name):
        if content: break
    else:
        print('No file with that name found in vault! Exiting...')
        return
    print('File found!')

    # Create list of attachments
    pattern = re.compile(r'!\[\[(.*?)\]\]')  # starting with ![[, ending with ]]
    for line in content:
        matches = pattern.finditer(line)
        if not matches: continue
        # Check if corresponding file in attachment, and append
        for match in matches:
            attachment = match.group(0)[3:-2]
            attachment_path = os.path.join(vault_from, attachments_from, attachment)
            if os.path.exists(attachment_path):
                destination_path = os.path.join(vault_to, attachments_to)
                if os.path.exists(destination_path): continue
                shutil.copy(attachment_path, destination_path)

    # Copy paste the file over
    file_name = file_name.lower() + ".md"
    destination_path = os.path.join(vault_to, file_name)
    shutil.copy(file_path, destination_path)

# Function vars  
vault_from = r"C:\Users\hk23402\My Drive\obsidian-vaults\uni-vault"
vault_to = r"C:\Users\hk23402\Desktop\Git_projects\mres-vault"
attachments_from = r"00 Attachments"
attachments_to = r"_Dictionary\_Attachments"

copy_file(file_name="Hippocampus", vault_from=vault_from, vault_to=vault_to, attachments_to=attachments_to, attachments_from=attachments_from)