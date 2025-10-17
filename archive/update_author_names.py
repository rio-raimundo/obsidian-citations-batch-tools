# %%
#! %load_ext autoreload
#! %autoreload 3
from collections import defaultdict

from pybtex.database import Entry, Person

from helpers import ObsidianNote, process_articles


# --- HELPER FUNCTIONS ---
def format_author(name: Person) -> str:
    return f"{name.first_names[0][0]}.{''.join(name.last_names)}".lower()

# - MAIN PROCESS FUNCTION TO POPULATE AUTHORS DICT --- 
@process_articles(limit=-1)
def find_similar_authors(obsidian_note: ObsidianNote):
    # Get our authors from the bibtex data as a list of Persons
    btex_data: Entry = obsidian_note.bibtex_data
    if 'author' not in btex_data.persons: return
    authors: list[Person] = btex_data.persons['author']

    for author in authors:
        authors_dict[format_author(author)].append(author)

# --- RUN MAIN FUNCTION 
authors_dict: dict[list] = defaultdict(list)
find_similar_authors()

# Construct the true author name 
true_author_names: dict[str] = {}
for author_key, author_names in authors_dict.items():
    fnames = set()
    for val in author_names: fnames.add(" ".join(val.first_names))

    mnames = []
    for val in author_names: mnames.append(val.middle_names)

    # In the longest set of middle names we have, if any of them are not just a single letter, we keep it
    middle_names_to_keep = []
    l_mnames = max(mnames, key=len)
    for mname in l_mnames:
        if len(mname) > 1 and mname[-1] != ".": middle_names_to_keep.append(mname)
    
    # Keep any prelast names
    plnames = []
    for val in author_names: plnames.append(val.prelast_names)
    prelast_names_to_keep = max(plnames, key=len, default=[])

    # Assemble the true name
    true_name = max(fnames, key=len)
    if middle_names_to_keep: true_name += f" {" ".join(middle_names_to_keep)}"
    if prelast_names_to_keep: true_name += f" {" ".join(prelast_names_to_keep)}"
    true_name += f" {" ".join(author_names[0].last_names)}"
    true_author_names[author_key] = true_name

    if "Berg" in val.last_names:
        pass

# Now we need to iterate BACK through and update all the author names
@process_articles(limit=-1)
def update_authors(obsidian_note: ObsidianNote):
    btex_data: Entry = obsidian_note.bibtex_data
    if 'author' not in btex_data.persons: return
    authors: list[Person] = btex_data.persons['author']

    new_authors = []
    for author in authors:
        true_name = true_author_names[format_author(author)]
        new_authors.append(true_name)

    obsidian_note.properties['authors'] = new_authors

update_authors()
