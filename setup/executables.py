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

def update_zotero_links(limit: int = -1, copy_files: bool = False):
    """ Update zotero links to the new format. """

    for file in yield_papers(limit=limit):
        file: ObsidianFile
        
        # Find citation key and zotero link
        citation_key = file.return_property_values('citation key')[0]
        
        # Find old format zotero link
        for link in file.return_property_values('links'):
            if 'zotero://select/' in link:
                zotero_link = link
                break
        
        # Replace and update properties
        new_zotero_link = f'zotero://select/items/@{citation_key}'
        file.replace_property_value(zotero_link, new_zotero_link)
        file.write_file(copy=copy_files)  # write files

def change_tags_to_lowercase(limit: int = -1, copy_files: bool = False):
    """ Change the word 'Tags' in the properties to 'tags', meaning that tags come up in search results. """

    for file in yield_papers(limit=limit):
        file: ObsidianFile
        file.make_properties_lowercase()
        file.write_file(copy=copy_files)  # write files

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

def update_DOIs_from_root_level_papers(limit: int = -1):
    """ Update broken DOI links using imported papers from the root level directory. """

    for root_level_paper in yield_papers(limit=limit, exclude_subfolders=True):
        root_level_paper: ObsidianFile
        
        # Get new DOI
        doi = root_level_paper.return_property_values('links')[0]
        
        # Find corresponding paper in the vault by matching citation key
        citation_key = root_level_paper.return_property_values('citation key')[0]
        
        for matching_paper in yield_papers():
            matching_paper: ObsidianFile
            old_link = matching_paper.return_property_values('links')[0]

            if matching_paper.return_property_values('citation key')[0] == citation_key and old_link != doi:
                matching_paper.replace_property_value(old_link, doi)
                matching_paper.write_file()
                break  # matching paper found, no need to keep iterating

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