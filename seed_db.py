"""Initialize the database for tables with no/minimal dependencies."""

import csv
import json
import os
from random import choice, randint
import sys

import crud
import model
from setup import read_files
# import server?

# os.system('. secrets.sh')  # fix this after figuring out API keys... in server.py

# Get name of the directory where this file is present.
current = os.path.dirname(os.path.realpath(__file__))
print(f'NOTE: current os.path.dirname(os.path.realpath(__file__)) = {current} for __file__ = {__file__}\n')

# Get name of the parent directory, relative to the current directory.
parent = os.path.dirname(current)
print(f'NOTE: parent = {parent}\n')

# Adding the parent directory to the sys.path.
sys.path.append(parent)

os.system('dropdb project_test --if-exists')
os.system('createdb project_test')

if __name__ == '__main__':
    import re
    from server import app
    if re.search(r'skincare$', current):
        print(f'NOTE: Imported app from server in current directory, which is {current}')
        print(f'NOTE: The parent directory is {parent}')
    else:
        print(f'NOTE: Imported app from parent.server, and the parent directory is {parent}')
    model.connect_to_db(app)
    model.db.create_all()
    
    # can use data/file_list_test2.txt to test
    files_to_load = 'data/file_list.txt'
    added_objects_dict = read_files.main(files_to_load)

    print(f'NOTE: list(added_objects_dict.keys()) = {list(added_objects_dict.keys())}')
    # app.run(host='0.0.0.0', debug=True)