""" Module for supporting callables which can be used for general purpose. These callables DON'T rely on constants.py.  """

# from .[FILE] import [CALLABLE]

from .obsidian_file import ObsidianFile
from .zotero_queries import doi_from_citation_key

__all__ = []  # list as strings