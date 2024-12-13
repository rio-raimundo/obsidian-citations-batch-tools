""" File allowing the batch renaming of notes. This is difficult to do normally because links are not updated if files are renamed outside of Obsidian. """
import re

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
    
    def replace_links(self, link: str):
        """ Checks if a given link is in the dictionary and replaces it with the new name. """
        if link in self.notes_to_rename:
            return self.notes_to_rename[link]
        return link
        
    def rename_files(self):
        """ Called once all files are accumulated. Time efficient because it checks every link in every file only once, against the dictionary (constant lookup time). """

        for obsidian_note in yield_notes(-1, exclude_subfolders=False):
            obsidian_note: ObsidianNote

            # Find all links in page
            for line in obsidian_note.body_text:
                re.sub(r"\[\[.*?\]\]", self.replace_links, line)