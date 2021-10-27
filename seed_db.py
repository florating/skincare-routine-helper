"""Initialize the database for tables with no/minimal dependencies."""

import os
# from random import choice, randint
import sys

from database import model, read_files

_DB_NAME_ = 'project_test_2'

# os.system('. secrets.sh')  # FIXME: after figuring out API keys
os.system(f'dropdb {_DB_NAME_} --if-exists')
os.system(f'createdb {_DB_NAME_}')


if __name__ == '__main__':
    import logging

    from server import app
    
    # when configuring logging explicitly, ensure all echo flags are set to False at all times, to avoid getting duplicate log lines
    # source: https://docs.sqlalchemy.org/en/14/core/engines.html#configuring-logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

    # Connect database to the Flask app in server.py and create all tables.
    model.connect_to_db(flask_app=app, db_uri=f"postgresql:///{_DB_NAME_}", echo=False)
    model.db.create_all()
    
    # Get filename of second argument, with instructions to seed the database.
    # Eg: python3 seed_db.py files_to_load
    files_to_load = sys.argv[1:]

    if not files_to_load:
        # Default: use data/file_list_test2.txt to test seeding the database
        files_to_load = os.path.abspath('./data/file_list.txt')

    added_objects_dict = read_files.main(files_to_load)
    
    print(f'NOTE: list(added_objects_dict.keys()) = {list(added_objects_dict.keys())}')
