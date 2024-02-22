import json 
import pickle as pkl
import pandas as pd

def write_file(data, extension, filename='data'):
    if extension not in ['json', 'csv', 'pkl']:
        raise ValueError("Invalid extension. Must be 'json', 'csv', or 'pkl'")
    
    if extension == 'pkl': 
        with open(filename + '.pkl', 'wb') as file:
            pkl.dump(data, file)
    elif extension == 'csv':
        data.to_csv(filename + '.csv')
    elif extension == 'json':
        with open(filename + '.json', 'w') as file:
            json.dump(data, file, indent=2)

def read_file(filename):
    extension = filename.split(".")[-1]
    if extension not in ['json', 'csv', 'pkl', 'md']:
        raise ValueError("Invalid extension. Must be 'json', 'csv', 'pkl' or 'md' file.")
    
    if extension == 'pkl': 
        with open(filename, 'rb') as file:
            return pd.read_pickle(filename)
    elif extension == 'csv':
        return pd.read_csv(filename)
    elif extension == 'json':
        with open(filename, 'r') as file:
            return json.load(file)
    elif extension == 'md':
        with open(filename, 'r', encoding='utf-8') as file:
            return file.read()