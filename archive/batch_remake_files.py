# %%
""" Script to update new files in an obsidian folder. """
import os
import glob
import re
import fnmatch
import warnings
from mistletoe import Document, HTMLRenderer

from file_utils import read_file
from file_iterator import FileIterator

def is_in_file(string: str, lines: list[str], return_line: bool = False):
    """ Checks if a string is present in a list of lines. If return_line is True, returns the index of the line. """
    for idx, line in enumerate(lines):
        if string in line:
            if return_line: return idx
            return True
    return False

def gen_filename_pattern(string: str) -> str:
    return r'\[\[.*' + string + r'*\]\]'

def replace_pattern_in_files(folder_path, pattern_to_search, new_name):
    for root, dirs, files in os.walk(folder_path):
        for file_name in fnmatch.filter(files, '*.md'):
            file_path = os.path.join(root, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check if the pattern is found in the content
            if re.search(pattern_to_search, content):
                # Use re.sub to replace the pattern with the new name
                new_content = re.sub(pattern_to_search, new_name, content)

                # Write the updated content back to the file
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(new_content)

                print(f"Pattern '{pattern_to_search}' replaced with '{new_name}' in file: {file_path}")

# Manually set folder path
vault_path = r"C:\Users\hk23402\Desktop\Git_projects\mres-vault"
folder_path = r"C:\Users\hk23402\Desktop\Git_projects\mres-vault\__General\Computational cognition\Papers"

# Generate list of all files (old and new) in folder
file_list = [os.path.basename(file) for file in glob.glob(f"{folder_path}/*.md")]

# Sort into new and old
new_filenames = [file for file in file_list if '(' in file]
old_filenames = [file[:-3] for file in file_list if '(' not in file]  # remove .md

# Main loop to process files
for filename in new_filenames:
    new_filepath = f"{folder_path}\\{filename}"

    # Read new file
    with open(new_filepath, 'r', encoding='utf-8') as new_file:
        new_lines = new_file.readlines()

    # Find citation key and check file of that name exists
    citation_idx = is_in_file('Citation Key', new_lines, return_line=True)
    if not citation_idx: 
        warnings.warn(f"Missing citation key in {filename}")
        continue
    citation_key = new_lines[citation_idx].split(": ")[1].strip()
    if citation_key not in old_filenames:
        continue

    # Read old file from citation key
    old_filepath = f"{folder_path}\\{citation_key}.md"
    with open(old_filepath, 'r', encoding='utf-8') as old_file:
        old_lines = old_file.readlines()
    
    # BUG: NEED TO SPLIT THESE LINES TO MAKE IT WORK
    
    # Take tags
    tag_iter = FileIterator('tags:', ':', include_first=False)

    # Copy summary and body
    if not is_in_file('# Summary', old_lines):
        # If no summary, just copy body text
        all_iter = FileIterator('---', ignore=1)
        for line in old_file:
            tag_iter.feed(line)
            all_iter.feed(line)
        summary_lines = []
    else:
        # If summary in file, copy summary and body
        feed_body = False
        sum_iter = FileIterator('# Summary', '#', include_first=False)
        body_iter = FileIterator('#')

        for line in old_lines:
            # Feed summary iterator. If just stopped, start new iter
            tag_iter.feed(line)
            if sum_iter.feed(line): feed_body = True
            if feed_body: body_iter.feed(line)
        summary_lines = sum_iter.text
    tag_lines, body_lines = tag_iter.text, body_iter.text

    # Add new lines to file
    # Add tags
    for tag_idx in range(len(new_lines)):
        if "  - paper" in new_lines[tag_idx]: break
    new_lines[tag_idx+1:tag_idx+1] = [f"{line}\n" for line in tag_lines]

    # Change summary
    for new_idx in range(len(new_lines)):
        if "[!my-summary] Summary" in new_lines[new_idx]: break
    del new_lines[new_idx+1]  # delete '-' line

    # Strip bullets from summary
    for sum_idx, line in enumerate(summary_lines):
        if line.startswith('- '):
            summary_lines[sum_idx] = line[2:]
        summary_lines[sum_idx] = f"> - {summary_lines[sum_idx]}"

    new_lines[new_idx+1:new_idx+1] = [f"{line}\n" for line in summary_lines if line != '> - ']
    new_lines += [f"{line}\n" for line in body_lines]

    # Write the file
    with open(f"{new_filepath}", 'w', encoding='utf-8') as file:
        file.writelines(new_lines)
    
    # Find all references to old name within a vault.
    replace_pattern_in_files(vault_path, pattern_to_search=gen_filename_pattern(citation_key), new_name=f"[[{filename}]]")

    # Delete old file 😳
    os.remove(old_filepath)
    print(f"---- Processed file {filename}!\n")
        





