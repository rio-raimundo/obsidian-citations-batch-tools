""" Contains functions at the highest level in the hierarchy of this project, to be called directly by the user in main.py as decorators to modify ObsidianNote objects, representing articles in a vault. 

Currently contains two decorators:
    - process_articles: Decorator to run a function across all Obsidian article files in a vault.
    - rename_articles: Decorator to rename articles in a vault according to a defined set of rules.
"""
from . import yield_articles, yield_notes, ObsidianNote, NoteRenamer

def process_articles(
        limit: int = -1,
        write: bool = True,
        yield_all_files: bool = False,
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
        write (bool): Whether to automatically write the new file after processing. If false, obsidian_file.write_file() must be called manually within the function.
    
    Returns:
        function: A function which takes the same arguments as the supplied function and runs it on each file.
    """
    def decorator(func):
        """ This is the 'decorator' function which takes in the function to be decorated, and returns the 'wrapper' function which does the same thing but with the added logic. """
        def wrapper():
            """ This is the wrapper function which will be run when we call the decorated function (after it has been decorated). It contains the decorated function, plus the additional logic. """
            yield_func = yield_notes if yield_all_files else yield_articles

            for note in yield_func(limit):
                note: ObsidianNote
                func(note)
                if write: note.write_file()
            print("Finished processing articles!")
        return wrapper
    return decorator

def rename_articles(
    limit: int = -1,
    yield_all_files: bool = False,
    ):
    """ Decorator factory to rename articles in a vault.

    Specifications:
        - Take an ObsidianNote object as an argument, with no other arguments.
        - Return statements MUST be in the form of a str "new_name", OR None to skip renaming the file.

    Example usage:
        @rename_articles(limit=-1, exclude_subfolders=False)
        def change_ands_to_ampersands(obsidian_article: ObsidianNote):
            if ' and ' in obsidian_article.filename:
                new_name = obsidian_article.filename.replace(' and ', ' & ')
                return new_name
            else:
                return None

    Args:
        limit (int): The number of files to process. If negative, will process all files.
    
    Returns:
        function: A function which takes the same arguments as the supplied function and runs it on each file.
    """
    def decorator(func):

        def wrapper():
            # First we initialise the renamer
            renamer = NoteRenamer() 

            # 'input' wrapper defined here so that we can call the function with the process_articles decorator
            @process_articles(limit=limit, write=False, yield_all_files=yield_all_files)
            def input_func_wrapper(note: ObsidianNote):
                # Call the decorated function: if it returns something, rename the file to this, otherwise do nothing.
                new_name = func(note)
                if new_name is not None:
                    new_name: str

                    # Strip the file extensions
                    old_name, new_name = note.filename.rsplit('.', 1)[0], new_name.rsplit('.', 1)[0]

                    # Strip the file extension from the new name
                    renamer.add(note.filepath, old_name, new_name)
            
            # Call our wrapped function which will add a list of desired files to the renamer
            input_func_wrapper()

            # Rename all the files by calling the function once in the renamer, on the list of files to rename
            renamer.rename_files()

        return wrapper
    return decorator

