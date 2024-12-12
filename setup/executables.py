# %%
""" General use functions to make edits to article files in the vault. """
from concurrent import futures

from helpers import ObsidianNote, doi_from_citation_key
from . import yield_articles

def toggle_abstract_collapsing(
        become_open: bool,
        limit: int = -1,
        copy_files: bool = False
        ) -> None:
    """
    Toggles open and closed abstract headers in each paper in a vault.

    Args:
        become_open (bool): Whether to open or close the abstract callout.
        limit (int): The number of files to process. If negative, will process all files.
        copy_files (bool): Whether to write the updated file to a new file.

    Returns:
        None
    """
    for article in yield_articles(limit=limit):
        article: ObsidianNote
        if article.property_contains_value('tags', 'stub'): continue  # keep stubs unfolded

        # Toggle abstract headers
        for idx, line in enumerate(article):
            line: str
            if not line.startswith("> [!my-abstract]"): continue

            # Toggle callout
            if become_open:
                article[idx] = line.replace("[!my-abstract]-", "[!my-abstract]+")
            else:
                article[idx] = line.replace("[!my-abstract]+", "[!my-abstract]-")
        
        article.write_file(copy=copy_files)

def add_author_names_as_tags(
        limit: int = -1,
        copy_files: bool = False,
    ) -> None:
    """Adds authors' names as tags by creating a tag with the name in the format
    'authors/<first-name>-<last-name>'.

    Args:
        limit: int
            The number of files to process. If negative, will process all files.
        copy_files: bool
            Whether to write the updated file to a new file.

    Returns:
        None
    """
    for article in yield_articles(limit=limit):
        article: ObsidianNote

        # Extract authors
        authors: list[str] = article.properties_dict.get('authors', None)
        if authors is None: continue

        for author in authors:
            author: str = author.lower()

            # Need to format the author page as a string
            parts: list[str] = author.split(' ')

            # First we remove parts with periods
            parts = [part for part in parts if '.' not in part]

            # Then we remove leftover single letters
            parts = [part for part in parts if len(part) > 1]

            tag: str = 'authors/' + '-'.join(parts)
            if tag in article.properties_dict.get('tags', []): continue
            article.properties_dict['tags'].append(tag)

        article._flat_properties_from_dict()
        article.write_file(copy=copy_files)

def reorder_properties(
        properties_order: list[str],
        limit: int = -1,
        copy_files: bool = False,
    ) -> None:
    """
    Reorders properties in a specified order.

    Args:
        properties_order (list[str]): The order in which to list properties. If a property is not in this list, it will remain in the current order at the end of the file.
        limit (int): The number of files to process. If negative, will process all files.
        copy_files (bool): Whether to write the updated file to a new file.

    Returns:
        None
    """
    for article in yield_articles(limit=limit):
        article: ObsidianNote

        listed_properties = {k: article.properties_dict[k] for k in properties_order if k in article.properties_dict}
        unlisted_properties = {k: v for k, v in article.properties_dict.items() if k not in properties_order}
        article.properties_dict = listed_properties | unlisted_properties
        article._flat_properties_from_dict()
        article.write_file(copy=copy_files)

def split_links_property(
        limit: int = -1,
        copy_files: bool = False
    ) -> None:
    """ Split old format 'links' property into 'DOI' and 'Zotero' properties.

    Args:
        limit (int): The number of files to process. If negative, will process all files.
        copy_files (bool): Whether to write the updated file to a new file.

    Returns:
        None
    """
    for paper in yield_articles(limit=limit):
        paper: ObsidianNote

        def find_first_starting_with(items: list[str], string: str) -> str:
            """ Find the first item in a list that starts with a given string. If none, returns empty string.

            Args:
                items (list[str]): The list to search
                string (str): The string to search for

            Returns:
                str: The first item in a list that starts with the given string. If none, returns empty string.
            """
            legal = [item for item in items if item.startswith(string)]
            if len(legal) == 0: return ""
            return legal[0]

        # Skip 'new' format papers which do not have links property
        try:
            links = paper.return_property_values('links')
        except KeyError:
            continue

        # Find relevant parameters
        doi = find_first_starting_with(links, 'https://doi.org/')
        zotero = find_first_starting_with(links, 'zotero')

        # Can modify file.properties directly and then update flat properties
        del paper.properties_dict['links']
        paper.properties_dict['doi'] = doi if doi else ""
        paper.properties_dict['zotero'] = zotero if zotero else ""
        paper._flat_properties_from_dict()
        paper.write_file(copy=copy_files)

def add_missing_dois(
        limit: int = -1,
        copy_files: bool = False
    ) -> None:
    """Add missing DOIs to papers in the vault. Interfaces with the Zotero API to retrieve DOIs, which is a slower method. Faster with better bibtex.

    Args:
        limit (int): The number of papers to process. If negative, will process all papers.
        copy_files (bool): Whether to write the updated file to a new file.

    Returns:
        None
    """
    papers = []
    for paper in yield_articles():
        if len(papers) == limit: 
            break
        paper: ObsidianNote
        if paper.properties_dict.get('doi', False) is False: 
            return
        if paper.properties_dict['doi'] is None: 
            papers.append(paper)

    def get_doi(paper: ObsidianNote) -> None:
        """Retrieve and update DOI for a paper.

        Args:
            paper (ObsidianFile): The paper object to update.
        """
        doi = doi_from_citation_key(paper.properties_dict['citation key'])
        print(f"Updating {paper.properties_dict['citation key']:15} with doi {doi}")
        paper.properties_dict['doi'] = doi
        paper._flat_properties_from_dict()
        paper.write_file(copy=copy_files)

    # Split into threads because the API request can take a long time
    executor = futures.ThreadPoolExecutor()
    threads = [executor.submit(get_doi, paper) for paper in papers]
    futures.wait(threads)
    print('done!')
