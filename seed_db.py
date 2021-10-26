"""Initialize the database for tables with no/minimal dependencies."""

import os
# from random import choice, randint
import sys

from database import model, read_files
# from setup import read_files

# os.system('. secrets.sh')  # FIXME: after figuring out API keys
os.system('dropdb project_test --if-exists')
os.system('createdb project_test')


if __name__ == '__main__':
    from server import app

    # Connect database to the Flask app in server.py and create all tables.
    model.connect_to_db(app)
    model.db.create_all()
    
    # Get filename of second argument, with instructions to seed the database.
    # Eg: python3 seed_db.py files_to_load
    files_to_load = sys.argv[1:]

    if not files_to_load:
        # Default: use data/file_list_test2.txt to test seeding the database
        files_to_load = os.path.abspath('./data/file_list.txt')

    added_objects_dict = read_files.main(files_to_load)
    
    print(f'NOTE: list(added_objects_dict.keys()) = {list(added_objects_dict.keys())}')
