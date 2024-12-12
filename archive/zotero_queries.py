import requests
import json
import re

def doi_from_citation_key(citation_key: str):
    """ Finds the doi associated with a given citation. Only works for one citation key at a time because of limitations with the API. """

    # Make POST request to local better-bibtex server.
    url = 'http://localhost:23119/better-bibtex/json-rpc'
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    """
    Parameters for item.bibliography:
        quickCopy (boolean): when true, use the QuickCopy setting from Zotero
        contentType (string): when present, must be html or text
        id (string): a CSL style name
    """
    data = {
        'jsonrpc': '2.0',
        'method': 'item.bibliography',
        'params': [[citation_key], {'id': 'apa'}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data)).json()

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
    except requests.exceptions.RequestException as e:
        return None

    result = response.json()['result']
    match = re.search(r"https:\/\/doi[^\s]*", result)
    if match is None: return None
    return match.group()  # find doi of paper