# %%
from concurrent import futures

from helpers import ObsidianFile, doi_from_citation_key
from . import yield_papers

def toggle_abstract_collapsing(become_open: bool, limit: int = -1, copy_files: bool = False):
    """ Toggles open and closed abstract headers in each paper in a vault. """
    for file in yield_papers(limit=limit):
        file: ObsidianFile
        if file.property_contains_value('tags', 'stub'): continue  # keep stubs unfolded

        # Toggle abstract headers
        for idx, line in enumerate(file):
            line: str
            if not line.startswith("> [!my-abstract]"): continue

            # Toggle callout
            if become_open:
                file[idx] = line.replace("[!my-abstract]-", "[!my-abstract]+")
            else:
                file[idx] = line.replace("[!my-abstract]+", "[!my-abstract]-")
        
        file.write_file(copy=copy_files)

def add_author_names_as_tags(limit: int = -1, copy_files: bool = False):
    for paper in yield_papers(limit=-1):
        paper: ObsidianFile

        # Extract authors
        authors = paper.properties.get('authors', None)
        if authors is None: continue

        for author in authors:
            author: str = author.lower()

            # Need to format the author page as a string
            parts = author.split(' ')

            # First we remove parts with periods
            parts = [part for part in parts if '.' not in part]

            # Then we remove leftover single letters
            parts = [part for part in parts if len(part) > 1]

            # Sanity check code to make sure we don't have any weird characters
            # for part in parts:
            #     for letter in part:
            #         if letter not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            #             print(parts)

            tag = 'authors/' + '-'.join(parts)
            if tag in paper.properties.get('tags', []): continue
            paper.properties['tags'].append(tag)

        paper.update_flat_properties_from_properties_dict()
        paper.write_file()

def reorder_properties(limit: int = -1, copy_files: bool = False):
    properties_order = [
        'title',
        'tags',
        'zotero',
        'doi',
        'authors',
        'citation key',
    ]

    for paper in yield_papers(limit=limit):
        paper: ObsidianFile

        for key, value in paper.properties.items():
            listed_properties = {k: paper.properties[k] for k in properties_order if k in paper.properties}
            unlisted_properties = {k: v for k, v in paper.properties.items() if k not in properties_order}
            paper.properties = listed_properties | unlisted_properties
            paper.update_flat_properties_from_properties_dict()
            paper.write_file(copy=copy_files)

def split_links_property(limit: int = -1, copy_files: bool = False):
    """ Split old format 'links' property into 'DOI' and 'Zotero' properties. """

    for paper in yield_papers(limit=limit):
        paper: ObsidianFile

        def find_first_starting_with(items: list[str], string: str):
            """ Find the first item in a list that starts with a given string. If none, returns empty string. """
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
        del paper.properties['links']
        paper.properties['doi'] = doi if doi else ""
        paper.properties['zotero'] = zotero if zotero else ""
        paper.update_flat_properties_from_properties_dict()
        paper.write_file(copy=copy_files)

def add_missing_dois(limit: int = -1, copy_files: bool = False):
    """ Add missing DOIs to papers in the vault. """
    papers = []
    for paper in yield_papers():
        if len(papers) == limit: break
        paper: ObsidianFile
        if paper.properties.get('doi', False) is False: return
        if paper.properties['doi'] is None: papers.append(paper)

    def get_doi(paper: ObsidianFile):
        doi = doi_from_citation_key(paper.properties['citation key'])
        print(f"Updating {paper.properties['citation key']:15} with doi {doi}")
        paper.properties['doi'] = doi
        paper.update_flat_properties_from_properties_dict()
        paper.write_file(copy=copy_files)

    # Split into threads bc the API request cna take ages
    executor = futures.ThreadPoolExecutor()
    threads = [executor.submit(get_doi, paper) for paper in papers]
    futures.wait(threads)
    print('done!')