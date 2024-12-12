""" A file for general functions which may be useful when modifying Obsidian notes. """

def get_value_from_bibtex_entry(citation_key: str, bibdata_entries: dict, value: str) -> str:
    """
    Gets a value from the local bibtex file for a given citation key and field.

    Args:
        citation_key (str): The citation key to search for.
        bibdata_entries (dict): The dictionary of entries read from the bibtex file.
        value (str): The name of the field to be retrieved.

    Returns:
        str: The value for the given citation key and field if it exists, None otherwise.
    """
    if citation_key not in bibdata_entries: return None
    if value not in bibdata_entries[citation_key].fields: return None
    return bibdata_entries[citation_key].fields[value]