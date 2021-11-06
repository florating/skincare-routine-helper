"""Initialize the database for tables with no/minimal dependencies."""

import os
from random import choice, randint
import sys

from database import crud, model, read_files

VALID_DB_NAMES = {'project_test', 'project_test_2', 'testdb'}


def create_users():
    """Return a list of created (and committed) users."""
    filepath = 'data/sample_datasets/users.csv'
    return read_files.load_csv('User', filepath)


if __name__ == '__main__':
    import logging

    from server import app
    
    # When configuring logging explicitly, ensure all echo flags are set to False at all
    # times, to avoid getting duplicate log lines
    # source: https://docs.sqlalchemy.org/en/14/core/engines.html#configuring-logging
    logging.basicConfig()
    logging.getLogger('sqlalchemy').setLevel(logging.ERROR)

    # Connect database to the Flask app in server.py and create all tables.
    model.connect_to_db(app, echo=False)
    model.db.create_all()
    
    _create_test = input('Do you want to add a test user? (Press Enter if not.) ')
    
    my_users = []

    if _create_test:
        test_user_params = {
            'f_name': 'Test',
            'l_name': 'Test',
            'email': 'test@test.com',
            'password': 'test',
            'skintype_id': 3,
            'primary_concern_id': 5
        }
        test_user = crud.create_user(**test_user_params)
        my_users.append(test_user)

    my_users.extend(create_users())
        
    print(f'Successfully added {len(my_users)} users to {_db_name}!')
