"""Initialize the database by loading data from files in the data directory."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv
import json

import crud


def load_files(table_obj_name, filename):
    """Load JSON or CSV files into the database.
    
    PARAMETERS:
        - table_obj_name (string): name of the table object (eg: 'Category')
        - filename (string): path to JSON or CSV file within the data directory

    RETURNS: a list of objects that were inserted into the database.
        - eg: [<Concern concern_id=1 ...>, <Concern concern_id=2 ...>]
    """
    if '.json' in filename:
        return load_json(table_obj_name, filename)
    elif '.csv' in filename:
        return load_csv(table_obj_name, filename)


def load_csv(table_obj_name, filename):
    """Read and load CSV files into the database.
    
    PARAMETERS:
        - table_obj_name (str): name of the table object (eg: 'Category')
        - filename (str): path to CSV file within the data directory

    RETURNS: a list of objects that were inserted into the database.
        - eg: [<Concern concern_id=1 ...>, <Concern concern_id=2 ...>]
    """
    print(f'\n\nStart loading data from {filename} into the {table_obj_name} table!\n\n')
    obj_in_db = []

    with open(f'data/{filename}', mode='r', encoding='utf-8-sig') as file:
        csvreader = csv.DictReader(file)

        # eg: row = {'concern_id': 1, 'concern_name': 'acne', ...}
        for row in csvreader:  
            obj = crud.create_table_obj(table_obj_name, **row)
            obj_in_db.append(obj)

    print(f'\n\nSuccessfully loaded {filename} into the {table_obj_name} table.\n\n')
    return obj_in_db


def load_json(table_obj_name, filename):
    """Read and load json files into the database.
    
    PARAMETERS:
        - table_obj_name (str): name of the table object (eg: 'Category')
        - filename (str): path to JSON file within the data directory

    RETURNS: a list of objects that were inserted into the database.
        - eg: [<Concern concern_id=1 ...>, <Concern concern_id=2 ...>]
    """
    obj_in_db = []

    with open(f'data/{filename}') as f:
        data = json.loads(f.read())

        for el in data:
            obj = crud.create_table_obj(table_obj_name, **el)
            obj_in_db.append(obj)
    
    print(f'Successfully loaded {filename} into the {table_obj_name} table.')
    return obj_in_db


def main(filename):
    """Given a text document with a list of table objects (table_obj_name) and filenames, read and load these files into the appropriate database tables.

    PARAMETERS:
        - filename (str): path to txt file within the data directory
            - the file at this location contains rows of text in this format:
            "table_object_name JSON_or_CSV_file_path"
                - eg: one line could say 'Concern skin_concerns.json'
                
    RETURNS:
        - added_objects (dict): a dictionary with the following key-value pairs:
            - keys = table object name (eg: 'Concern')
            - values = a list of objects added to the database (eg: a Concern object)
        -eg: {'Concern': [<Concern concern_id=1 ...>, <Concern concern_id=2 ...>]}
    """

    file_dict = {}
    added_objects_dict = {}
    print(f"filename = {filename}")
    with open(filename, 'r') as f:
        data = f.readlines()
        for line in data:
            class_name, filepath = line.split()
            file_dict[class_name] = filepath

    for tab_obj_name, file_path in file_dict.items():
        added_objects_dict[tab_obj_name] = load_files(tab_obj_name, file_path)
    return added_objects_dict
