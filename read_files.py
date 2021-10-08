import csv, json
import crud

TABLES_NO_DEPENDENCIES = {
    'Category',
    'Concern',
    'Ingredient',
    'SkincareStep',
    'Skintype'
}

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
        - table_obj_name (string): name of the table object (eg: 'Category')
        - filename (string): path to CSV file within the data directory

    RETURNS: a list of objects that were inserted into the database.
        - eg: [<Concern concern_id=1 ...>, <Concern concern_id=2 ...>]
    """
    header = []
    obj_in_db = []
    with open(f'data/{filename}', mode='r', encoding='utf-8-sig') as file:
        # Create a csv.reader object to read the csv file.
        csvreader = csv.reader(file)  # delimiter?

        header = next(csvreader)  # eg: header = ['Column1', 'Column2']
        obj_params = {}

        for row in csvreader:  # eg: row = ['1', 'hello']
            for i, header_field in enumerate(header):
                print(f'row={row}, i={i}')
                print(f'for i={i}: row[i]={row[i]}')
                print('*' * 20)
                print()
                obj_params[header_field] = row[i]  # row is 0-index
            
            if table_obj_name in TABLES_NO_DEPENDENCIES:
                obj = crud.create_table_obj(table_obj_name, **obj_params)
                print(f'obj={obj}')
                print('Time to go on to the next row or something!\n\n')
                obj_in_db.append(obj)
            else:
                pass
        
    print(f'Successfully loaded {filename} into the {table_obj_name} table.')
    return obj_in_db


def load_json(table_obj_name, filename):
    """Read and load json files into the database.
    
    PARAMETERS:
        - table_obj_name (string): name of the table object (eg: 'Category')
        - filename (string): path to JSON file within the data directory

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


def create_complex_obj(table_obj_name):
    # For Product:
        # Setup Ingredient object table first.
        # Setup Product
        # Setup ProductIngredient object table.
    # For Interaction:
        # Setup Ingredient object table first.
    # 
    pass



def main(filename):
    """Given a text document with a list of table objects (table_obj_name) and filenames, read and load these files into the appropriate database tables.
    
    PARAMETERS:
        - filename (string): path to txt file within the data directory containing rows of table object name and JSON/CSV file path
        - eg: one line could say 'Concern skin_concerns.json'

    RETURNS:
        - added_objects (dict): a dictionary with the following key-value pairs:
            - keys = table object name (eg: 'Concern')
            - values = a list of objects added to the database (eg: a Concern object)
        -eg: {'Concern': [<Concern concern_id=1 ...>, <Concern concern_id=2 ...>]}
    """

    file_dict = {}
    added_objects = {}

    with open(filename) as f:
        data = f.readlines()
        for line in data:
            key, val = line.split()
            file_dict[key] = val

    for tab_obj_name, filename in file_dict.items():
        added_objects[tab_obj_name] = load_files(tab_obj_name, filename)
    return added_objects
