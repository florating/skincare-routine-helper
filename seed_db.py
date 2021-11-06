"""Initialize the database for tables with no/minimal dependencies."""

import os
# from random import choice, randint
import sys

from database import model, read_files

VALID_DB_NAMES = {'project_test', 'project_test_2', 'testdb'}


if __name__ == '__main__':
    import logging

    from server import app
    
    _db_name = input('What is the name of the PostgreSQL database?  ')

    # TODO: check if this is still fine
    if _db_name in VALID_DB_NAMES:
        os.system(f'dropdb {_db_name} --if-exists')
        os.system(f'createdb {_db_name}')

        # When configuring logging explicitly, ensure all echo flags are set to False at all
        # times, to avoid getting duplicate log lines
        # source: https://docs.sqlalchemy.org/en/14/core/engines.html#configuring-logging
        logging.basicConfig()
        logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

        # Connect database to the Flask app in server.py and create all tables.
        model.connect_to_db(app, echo=False)
        model.db.create_all()
    
        # Get filename of second argument, with instructions to seed the database.
        files_to_load = os.path.abspath('./data/file_list.txt')

        added_objects_dict = read_files.main(files_to_load)
    
        print(f'NOTE: list(added_objects_dict.keys()) = {list(added_objects_dict.keys())}')
    else:
        print('That is not a valid database name. Sorry.')
