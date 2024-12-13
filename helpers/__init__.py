""" Module for supporting callables which can be used for general purpose. These callables DON'T rely on constants.py.  """

# from .[FILE] import [CALLABLE]

from .obsidian_note import ObsidianNote
from .yield_functions import yield_files, yield_notes, yield_articles, process_articles
from .note_renamer import NoteRenamer
from .general_functions import *
from .examples import *

__all__ = []  # list as strings