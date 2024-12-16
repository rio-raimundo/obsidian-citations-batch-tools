""" Contains functions at the highest level in the hierarchy of this project, to be called directly by the user in main.py as decorators to modify ObsidianNote objects, representing articles in a vault. 

Currently contains two decorators:
    - process_articles: Decorator to run a function across all Obsidian article files in a vault.
    - rename_articles: Decorator to rename articles in a vault according to a defined set of rules.
"""
from . import yield_articles, ObsidianNote, NoteRenamer

def process_articles(
        limit: int = -1,
        exclude_subfolders: bool = False,
        write: bool = True,
        ):
    """ Decorator factory to run a function across all Obsidian article files in a vault.

    Specifications:
        - Take an ObsidianNote object as an argument, with no other arguments.
        - Return statements can be given, but will be ignored. The decorated function will return None.

    Example usage:
        @process_articles(limit=-1, exclude_subfolders=False, write=True)
        def delete_journal_property(obsidian_note: ObsidianNote):
            if 'journal' in obsidian_note.properties:
                del obsidian_note.properties['journal']
    
    Args:
        limit (int): The number of files to process. If negative, will process all files.
        exclude_subfolders (bool): Whether to exclude subfolders of the main folder.
        write (bool): Whether to automatically write the new file after processing. If false, obsidian_file.write_file() must be called manually within the function.
    
    Returns:
        function: A function which takes the same arguments as the supplied function and runs it on each file.
    """
    def decorator(func):
        """ This is the 'decorator' function which takes in the function to be decorated, and returns the 'wrapper' function which does the same thing but with the added logic. """
        def wrapper():
            """ This is the wrapper function which will be run when we call the decorated function (after it has been decorated). It contains the decorated function, plus the additional logic. """
            for obsidian_article in yield_articles(limit, exclude_subfolders):
                obsidian_article: ObsidianNote
                if write: obsidian_article.write_file()
            print("Finished processing articles!")
        return wrapper
    return decorator



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
        def wrapper():
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
