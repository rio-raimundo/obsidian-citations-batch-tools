# %%
#! %load_ext autoreload
#! %autoreload 3
""" Main file from which to run the project."""


from multiprocessing import process
from helpers import ObsidianNote, process_articles, rename_articles
import constants as c
from pybtex.database import Person, Entry
from pybtex.richtext import Text
from pybtex.utils import OrderedCaseInsensitiveDict

journal_abbrevs = {
        "Canadian Journal of Experimental Psychology / Revue canadienne de psychologie expérimentale": "CJEP",
        "Journal of Experimental Psychology: Human Perception and Performance": "J Exp Psychol Hum Perf",
        "Psychonomic Bulletin & Review": "Psychon Bull Rev",
        "Nature Neuroscience": "Nat Neurosci",
        "Journal of Mathematical Psychology": "Journal of Mathematical Psychology",
        "Nature": "Nature",
        "Psychological science": "Psychol Sci",
        "Proceedings of the National Academy of Sciences of the United States of America": "PNAS USA",
        "Journal of Vision": "J Vision",
        "Science": "Science",
        "The Journal of Neuroscience": "J Neurosci",
        "British Journal of Psychology": "BJ Psychol",
        "Neuron": "Neuron",
        "Behavioral and Brain Sciences": "Behav Brain Sci",
        "Topics in Cognitive Science": "TICS",
        "Vision Research": "Vision Research",
        "Current Biology": "Curr Biology",
        "Frontiers in Psychology": "Front Psychol",
        "Frontiers in Human Neuroscience": "Front Hum Neurosci.",
        "Current Opinion in Neurobiology": "Curr Opinion Neurobio",
        "Proceedings of the National Academy of Sciences": "PNAS",
        "Journal of Neuroscience": "J Neurosci",
        "Nature Human Behaviour": "Nat Hum Behav",
        "Psychological Bulletin": "Psychol Bull",
        "Communications Biology": "Commun Biol",
        "Journal of Cerebral Blood Flow & Metabolism": "J Cereb Blood Flow Metab",
        "Nature Communications": "Nat Commun",
        "Nature Reviews Neuroscience": "Nat Rev Neurosci",
        "Trends in Cognitive Sciences": "TiCS",
        "Neural Computation": "Neural Computation",
        "Psychological Science": "Psychol Sci",
        "Cognition": "Cognition",
        "Psychological Review": "Psychol Review",
        "NeuroImage": "NeuroImage",
        "eLife": "eLife",
        "Neuroscience & Biobehavioral Reviews": "NaBR",
        "Communications Psychology": "Commun Psychol",
        "Frontiers in Neuroscience": "Front Neurosci",
        "Trends in Neurosciences": "TiNS",
        "Annual Review of Neuroscience": "Ann Rev Neurosci",
        "PLOS Computational Biology": "PLOS Comp Bio",
        "Cerebral Cortex (New York, N.Y.: 1991)": "Cereb Cortex",
        "Cognitive, Affective, & Behavioral Neuroscience": "Cogn Affect Behav Neurosci",
    }

# %% 
""" Check all files with no bibdata. """
@process_articles(limit=-1, write=False)
def check_files(obsidian_note: ObsidianNote):
    bibdata: Entry = obsidian_note.bibtex_data
    if not bibdata:
        print(obsidian_note.filepath)
        pass

check_files()

# %%

@rename_articles(limit=-1)
def rename_files(obsidian_note: ObsidianNote):
    bibdata: Entry = obsidian_note.bibtex_data
    if not bibdata:  return
    fields: OrderedCaseInsensitiveDict = bibdata.fields
    
    # Get author names in desired format
    authors: list[Person] = bibdata.persons['author']
    author_names = authors[0].rich_last_names[0]
    if len(authors) > 1: author_names += f"; {authors[-1].rich_last_names[0]}"

    # Get the year
    year = fields['year']
    
    # Get the journal
    if fields.get('journal'):
        journal = str(Text.from_latex(fields['journal']))
        # Feed it through our list
        journal = journal_abbrevs.get(journal, journal)
    elif fields.get('publisher'):
        journal = fields['publisher']
    else: 
        journal = "Unlisted"
    journal = journal.translate(str.maketrans('', '', '*"\\/<>:|?'))
    
    # Join it all together
    new_name = f"{year} {author_names} ({journal}).md"
    print(new_name)
    if obsidian_note.filename != new_name: return new_name

# Call the function
rename_files()