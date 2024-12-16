""" File allowing the batch renaming of notes. This is difficult to do normally because links are not updated if files are renamed outside of Obsidian. Includes the note renamer class and a special decorator to process all articles in a vault. """
import regex

from dataclasses import dataclass
from . import yield_notes, ObsidianNote

@dataclass
class FileRef:
    """ Dataclass representing a reference to a file. """
    filepath: str
    old_name: str
    new_name: str

class NoteRenamer:
    def __init__(self):
        self.notes_to_rename: dict = {}

    def add(self, filepath: str, old_name: str, new_name: str):
        """ Adds a new renaming to the list of renamings. """
        # First, move the file to a different location
        obsidian_note = ObsidianNote(filepath)
        obsidian_note.replace_file(filepath.replace(old_name, new_name))

        # Then add the renaming to the dictionary
        self.notes_to_rename[old_name] = new_name

    def replace_link(self, link: str):
        """ Checks if a given link is in the dictionary and replaces it with the new name. """
        if link in self.notes_to_rename:
            return self.notes_to_rename[link]
        return link
        
    def rename_files(self):
        """ Called once all files are accumulated. Time efficient because it checks every link in every file only once, against the dictionary (constant lookup time). """

        for obsidian_note in yield_notes(-1, exclude_subfolders=False):
            obsidian_note: ObsidianNote

            """ First we can define the regex patterns which will be used:
                - Full link pattern is a simple pattern that matches any text in the form [[...]], including the brackets

                - Link name pattern is a complex pattern attempting to match the 'true link' portion of linked text (referred to as 'l'):
                    - This includes cases of links to headings ('l#'), links to blocks ('l#^'), links with renames ('l|'), links in tables ('l\|'), and absolute links ('/l').
                    - The link has three main parts. First is a lookbehind matching either '[[' or '/' (the start of a link).
                    - Second is the actual link name, which is any text that is not '#', '|', '/' or '\' (the end of a link).
                    - Finally, there is a lookahead matching either ']]', '|', '#', or '\' (the end of a link).
             """
            full_link_pattern = regex.compile(r"\[\[.*?\]\]")
            link_name_pattern = regex.compile(r"(?<=\[\[|\/)[^#|\/\\]*(?=\]\]|\||#|\\)")

            # Iterate through each line of the note and check links
            for idx in range(len(obsidian_note.body_text)):
                full_links = regex.findall(full_link_pattern, obsidian_note.body_text[idx])
                
                # For each link, including the brackets
                for full_link in full_links:
                    # we have to pull out the link name, accounting for all possible phrasings (absolute links, links to headings, links with renames, etc.)
                    # This can be done using the link_name_pattern - can put this into regex101.com to see how it works
                    link_name = regex.search(link_name_pattern, full_link).group(0)

                    # Get the 'new' link name (replaces old name with new name if it exists, otherwise just returns the old name)
                    new_link_name = self.replace_link(link_name)

                    # Sub the new link name into the full link only at the occurrences given by the link_name_pattern
                    new_full_link = regex.sub(link_name_pattern, new_link_name, full_link)
                    
                    # Replace the full link in the text with the new full link
                    if new_full_link != full_link:
                        obsidian_note.body_text[idx] = obsidian_note.body_text[idx].replace(full_link, new_full_link)
            
            # Write the file
            obsidian_note.write_file()