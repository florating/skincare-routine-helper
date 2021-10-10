"""Test crud functions.

To join a session into an external transaction (for a test suite?), check out this resource:
https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
"""

import os
import sys
from unittest import TestCase

from werkzeug.security import generate_password_hash, check_password_hash

# Get name of the directory where this file is present.
current = os.path.dirname(os.path.realpath(__file__))
print(f'NOTE: current os.path.dirname(os.path.realpath(__file__)) = {current} for __file__ = {__file__}\n')

# Get name of the parent directory, relative to the current directory.
parent = os.path.dirname(current)
print(f'NOTE: parent = {parent}\n')

# Adding the parent directory to the sys.path.
sys.path.append(parent)

import crud
import model
from model import db, Skintype, User, Concern
from server import app


class TestCrudDatabase(TestCase):
    """Crud tests that use the database."""

    def setUp(self):
        os.system('dropdb testdb --if-exists')
        os.system('createdb testdb')
        model.connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        example_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_setUp_and_tearDown(self):
        """Test if setUp and tearDown methods are working."""
        self.assertEqual('a', 'a')
    
    def test_get_user_by_email(self):
        test_query = User.query.filter_by(email='email_1@email.com').first()
        test_user = crud.get_user_by_email('email_1@email.com')
        self.assertEqual(test_user, test_query)
    
    def test_create_table_obj(self):
        """Check that object has been added to the database."""
        table_class_name = 'Concern'
        obj_params = {
            "concern_name": "anti-aging",
            "description": "Fine lines & sun damage"
        }
        test_obj = crud.create_table_obj(table_class_name, **obj_params)
        test_query = Concern.query.filter_by(concern_name = "anti-aging").first()
        print(f"test_obj = {test_obj}, test_query = {test_query}")
        self.assertEqual(test_obj, test_query)


def example_data():
    """Generate example data for testing purposes."""

    # In case this is run more than once, empty out existing data
    Skintype.query.delete()
    User.query.delete()

    # Add sample skintypes and users
    sk1 = Skintype(skintype_name='combination', description='desc1')
    sk2 = Skintype(skintype_name='dry', description='desc2')
    sk3 = Skintype(skintype_name='normal', description='desc3')
    sk4 = Skintype(skintype_name='oily', description='desc4')

    user1 = User(f_name='Liz', email='email_1@email.com', hashed_password=generate_password_hash('pass_1'), skintype=sk2)
    user2 = User(f_name='Nadine', email='email_2@email.com', hashed_password=generate_password_hash('pass_2'), skintype=sk1)
    user3 = User(f_name='Bob', email='email_3@email.com', hashed_password=generate_password_hash('pass_3'), skintype=sk3)
    user4 = User(f_name='Jimmy', email='email_4@email.com', hashed_password=generate_password_hash('pass_4'), skintype=sk1)
    user5 = User(f_name='Alice', email='email_5@email.com', hashed_password=generate_password_hash('pass_5'), skintype=sk3)

    db.session.add_all([sk1, sk2, sk3, sk4])
    db.session.add_all([user1, user2, user3, user4, user5])
    db.session.commit()


if __name__ == "__main__":
    import unittest
    unittest.main()
