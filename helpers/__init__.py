""" Module for supporting callables which can be used for general purpose. These callables DON'T rely on constants.py.  """

# from .[FILE] import [CALLABLE]

from .obsidian_note import ObsidianNote
from .yield_functions import yield_files, yield_articles
from .examples import *

__all__ = []  # list as strings