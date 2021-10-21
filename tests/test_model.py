"""Test model functions.

To join a session into an external transaction (for a test suite?), check out this resource:
https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
"""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from unittest import TestCase

from werkzeug.security import generate_password_hash, check_password_hash

import crud
import model
from model import db, Concern, Ingredient, Product, ProductIngredient, Skintype, User
from server import app


class TestModelDatabase(TestCase):
    """Crud tests that use the database."""

    def setUp(self):
        os.system('dropdb testdb --if-exists')
        os.system('createdb testdb')
        model.connect_to_db(app, 'postgresql:///testdb')
        db.create_all()
        # example_data()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()
    
    def test_setUp_and_tearDown(self):
        """Test if setUp and tearDown methods are working."""
        self.assertEqual('a', 'a')
    
    # def test_get_user_by_email(self):
    #     test_query = User.query.filter_by(email='email_1@email.com').first()
    #     test_user = crud.get_user_by_email('email_1@email.com')
    #     self.assertEqual(test_user, test_query)
     
    # def test_get_first_obj_by_param(self):
    #     trad_queried_prod = model.User.query.get(1)
    #     query_param = {
    #         "user_id": 1
    #     }
    #     crud_queried_prod = crud.get_first_obj_by_param("User", **query_param)
    #     self.assertEqual(trad_queried_prod, crud_queried_prod)
    
    # def test_create_user(self):
    #     obj_params = {
    #         "email": "sqrpnts@gmail.com",
    #         "password": "Pineapple4!",
    #         "f_name": "Spongebob",
    #         "l_name": "Squarepants"
    #     }
    #     new_user = crud.create_user(**obj_params)
    #     queried_user = crud.get_user_by_email("sqrpnts@gmail.com")
    #     self.assertEqual(new_user, queried_user)
    
    def test_create_product_cascade(self):
        obj_params = {
            "product_name": "Generic Lotion",
            "product_type": "Moisturizer",
            "clean_ingreds": "['ingred_1', 'ingred_2', 'ingred_3']"
        }

        query_param = {
            "product_name": "Generic Lotion"
        }

        new_prod = crud.create_product_cascade(**obj_params)
        queried_prod = crud.get_first_obj_by_param("Product", **query_param)
        self.assertEqual(new_prod, queried_prod)

    def test_create_product_cascade_ingredients(self):
        """Test object creation cascade for products -> ingredients -> product_ingredients tables.
        SOURCE: https://docs-sqlalchemy.readthedocs.io/ko/latest/orm/cascades.html
        """
        params = {
            "product_name": "Facial Lotion",
            "brand_name": "Aveeno",
            "product_type": "Moisturizer",
            "clean_ingreds": "['ingred1', 'ingred2', 'ingred3', 'ingred4']"
        }
        clean_ingreds_list = crud.convert_string_to_list(params.pop("clean_ingreds"))
        ingreds_obj_list = []
        proding_obj_list = []
        for i, item in enumerate(clean_ingreds_list):
            # FIXME: what if the ingredient already exists in the ingredients table?
            ing_obj = Ingredient(common_name=item)
            ingreds_obj_list.append(ing_obj)
            obj2 = ProductIngredient(abundance_order=(i + 1))
            proding_obj_list.append(obj2)
            obj2.ingredient = ing_obj
        prod_obj = Product(**params)
        prod_obj.product_ingredients = proding_obj_list
        print("*"*20)
        print("*"*20)
        print(f"\nprod_obj.product_ingredients = proding_obj_list \
            \n prod_obj.product_ingredients = {prod_obj.product_ingredients}, \
            \n proding_obj_list = {proding_obj_list}\n\n")
        sess = db.session
        sess.add(prod_obj)
        print(f"prod_obj in sess --> {prod_obj in sess}")
        print(f"\ningreds_obj_list[0] --> {ingreds_obj_list[0]}")
        print(f"ingreds_obj_list[0] in sess --> {ingreds_obj_list[0] in sess}")
        sess.commit()
        print("*"*20)
        print("*"*20)
        print("Session committed!")
        print("*"*20)
        print("*"*20)
        self.assertEqual(ingreds_obj_list[0], proding_obj_list[0].ingredient)
        self.assertEqual(prod_obj, proding_obj_list[0].product)
        print(f"ingreds_obj_list[0] = {ingreds_obj_list[0]}, \
            \nproding_obj_list[0].ingredient = {proding_obj_list[0].ingredient}")
        print("*"*20)
        print(f"prod_obj = {prod_obj}, \
            \nproding_obj_list[0].product = {proding_obj_list[0].product}")
        print("*"*20)
        print("*"*20)


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
