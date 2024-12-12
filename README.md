A set of text tools written in Python for editing Obisidan pages meant to represent academic articles (i.e. taken from the Zotero Citations plugin). Allows for renaming of files, reorganising properties (including tags), and more customisation options. Can also allow interfacing with BibTex (`.bib`) files to extract and attach information to files from an existing bibliography. Initially intended purely for personal use, so documentation and code generalisability may vary.

> NOTE: Mass modification of Obsidian files can easily lead to data loss. It is highly recommended that you implement some kind of version control to your vault before using the tools provided here (personally, I highly recommend using [GitHub](https://github.com/Vinzent03/obsidian-git) to back up your vault!)

## Setting up the repository
To use this repo:
- Clone the `main` branch (designed for general use) locally onto your machine.
- Manually modify the values in `constants.py` to assign the correct paths.
- To use some of the repo's functionality, a link to a `BetterBibtex` `.bib` file will need to be provided.
    - [These steps](https://github.com/hans/obsidian-citation-plugin) intended for the Obsidian `Citations` plugin can be used to generate an automatically-updating Bibtex file, which can be placed in your vault and linked to via this repo.
    - These steps are intended for users of Zotero. If other reference managers are used, there are likely other ways to generate the needed Bibtex file.
    - Generally speaking, if you only need to rearrange existing information in your vault, you will not need to generate this file. However, it allows you to pull in new information about articles.

## Using the repository
The repository is designed to make the mass management of Obsidian files representing articles easier. The general usecase is as follows:
- Users can write a short custom function detailing the changes they want to make to a single `ObsidianFile`.
- They can leverage existing functionality of the custom `ObsidianFile` class, including automatic access of the file properties in dictionary structure and other functions, such as reordering properties.
- Custom functions can be flexibly applied to all Obsidian article notes in a vault by leveraging the `yield_articles` decorator, which runs a function across all files in an Obsidian vault with any of a specific set of tags. These tags can be set in `constants.py`.
- Example usage is provided at the top of the `main.py` script.
