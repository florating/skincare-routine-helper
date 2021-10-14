"""Initialize the database for tables with no/minimal dependencies."""

import os
# from random import choice, randint
import re
import sys

import model
from setup import read_files

# os.system('. secrets.sh')  # fix this after figuring out API keys... in server.py

# Get name of the directory where this file is present.
current = os.path.dirname(os.path.realpath(__file__))
print(f'NOTE: current os.path.dirname(os.path.realpath(__file__)) = {current} for __file__ = {__file__}\n')


# If the current filepath does not end in the word "skincare" (because we are in a nested directory)...
# and assuming the root directory named 'skincare' is one level above this one (at most),
# then perform the following actions:
if not re.search(r'skincare$', current):
    # Get name of the parent directory, relative to the current directory this file is in.
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
    
    # Get filename of second argument, with instructions to seed the database.
    # Eg: python3 seed_db.py files_to_load
    files_to_load = sys.argv[1:]

    if not files_to_load:
        # Default: use data/file_list_test2.txt to test seeding the database
        files_to_load = os.path.abspath('./data/file_list.txt')

    added_objects_dict = read_files.main(files_to_load)
    
    print(f'NOTE: list(added_objects_dict.keys()) = {list(added_objects_dict.keys())}')
