import csv, json
import crud


def load_files(table_obj, filename):
    """Load json or csv files.
    
    Returns a list of table_obj objects that were inserted into the database.
    """
    if '.json' in filename:
        return load_json(table_obj, filename)
    elif '.csv' in filename:
        return load_csv(table_obj, filename)


def load_csv(table_obj, filename):
    """Read and load json files into the database.
    
    Returns a list of table_obj objects that were inserted into the database.
    """
    header = []
    obj_in_db = []
    with open(f'data/{filename}') as file:
        # Create a csv.reader object to read the csv file.
        csvreader = csv.reader(file)  

        header = next(csvreader)  # eg: header = ['Column1', 'Column2']
        obj_params = {}

        for row in csvreader:  # eg: row = ['1', 'hello']
            for i, header_field in enumerate(header):
                obj_params[header_field] = row[i]  # row is 0-index
        obj = crud.create_table_obj(table_obj, **obj_params)
        obj_in_db.append(obj)
    print(f'Successfully loaded {filename} into the {table_obj} table.')
    return obj_in_db


def load_json(table_obj, filename):
    """Read and load json files into the database.
    
    Returns a list of table_obj objects that were inserted into the database.
    """
    obj_in_db = []
    with open(f'data/{filename}') as f:
        data = json.loads(f.read())
        for el in data:
            obj = crud.create_table_obj(table_obj, **el)
            obj_in_db.append(obj)
    print(f'Successfully loaded {filename} into the {table_obj} table.')
    return obj_in_db


def main(filename):
    """Given a text document with a list of table objects (table_obj) and filenames, read and load these files into the appropriate database tables.
    
    Returns a dictionary such that:
        - keys = table object name (eg: 'Concern')
        - values = list of objects added to the database (eg: a Concern object)
    """

    file_list = {}
    added_objects = {}

    with open(filename) as f:
        data = f.readlines()
        for line in data:
            key, val = line.split()
            file_list[key] = val

    for tab_obj, filename in file_list.items():
        added_objects[tab_obj] = load_files(tab_obj, filename)
    return added_objects
