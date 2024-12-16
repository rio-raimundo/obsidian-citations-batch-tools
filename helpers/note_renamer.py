""" File allowing the batch renaming of notes. This is difficult to do normally because links are not updated if files are renamed outside of Obsidian. Includes the note renamer class and a special decorator to process all articles in a vault. """
import regex

from dataclasses import dataclass
from . import yield_notes, ObsidianNote, process_articles

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
                    print(f"{obsidian_note.filename}: {link_name} -> {new_link_name}")

                    # Sub the new link name into the full link only at the occurrences given by the link_name_pattern
                    new_full_link = regex.sub(link_name_pattern, new_link_name, full_link)
                    
                    # Replace the full link in the text with the new full link
                    obsidian_note.body_text[idx] = obsidian_note.body_text[idx].replace(full_link, new_full_link)
            
            # Write the file
            obsidian_note.write_file()


# Decorator to rename articles in a vault
# REMEMBER: outermost function is just so you can pass arguments to the decorator
def rename_articles(
    limit: int = -1,
    exclude_subfolders: bool = False,
    ):
    """ Decorator factory to rename articles in a vault. """

    # This is the actual decorator, which can only take in a function
    def decorator(func):
        """ Decorator to run a function across all Obsidian article files in a vault."""

        # This is the wrapper function, which is actually going to execute the logic surrounding the function
        def wrapper(obsidian_note: ObsidianNote):
            # First we initialise the renamer
            renamer = NoteRenamer()

            # Define a new wrapper function which simply calls the input function ONCE, and then writes its output to the renamer
            # But remember, we DON'T write the files here, we just add them to the renamer, because it's faster to handle this logic all at once at the end
            @process_articles(limit=limit, exclude_subfolders=exclude_subfolders, write=False)
            def input_func_wrapper(obsidian_article: ObsidianNote):
                result = func(obsidian_article)
                if result is not None:
                    old_name, new_name = result
                    renamer.add(obsidian_article.filepath, old_name, new_name)
            
            # Now we call our wrapped function, which will call our input for each file in the vault
            # This adds to the note renamer a list of all the filepaths
            input_func_wrapper()

            # Rename all the files by calling the function once in the renamer, on the list of files to rename
            renamer.rename_files()

        return wrapper

    return decorator
