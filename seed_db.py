"""Initialize the database for tables with no/minimal dependencies."""

import os
# from random import choice, randint
import re
import sys

import model
from setup import read_files
# import server?

# os.system('. secrets.sh')  # fix this after figuring out API keys... in server.py

# Get name of the directory where this file is present.
current = os.path.dirname(os.path.realpath(__file__))
print(f'NOTE: current os.path.dirname(os.path.realpath(__file__)) = {current} for __file__ = {__file__}\n')

# Add parent directory if this file is currently in a nested directory.
# Assume root directory named 'skincare' is, at most, one level above this one.
if not re.search(r'skincare$', current):
    # Get name of the parent directory, relative to the current directory.
    parent = os.path.dirname(current)
    print(f'NOTE: parent = {parent}\n')

    # Adding the parent directory to the sys.path.
    sys.path.append(parent)

os.system('dropdb project_test --if-exists')
os.system('createdb project_test')

if __name__ == '__main__':
    from server import app

    # Connect database to the Flask app in server.py and create all tables.
    model.connect_to_db(app)
    model.db.create_all()
    
    # Get filename if another file path is given to use as instructions to seed the database
    # Eg: python3 seed_db.py files_to_load
    files_to_load = sys.argv[1:]

    if not files_to_load:
        # Default: use data/file_list_test2.txt to test seeding the database
        files_to_load = 'data/file_list.txt'

    added_objects_dict = read_files.main(files_to_load)
    print(f'NOTE: list(added_objects_dict.keys()) = {list(added_objects_dict.keys())}')

    # app.run(host='0.0.0.0', debug=True)