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

import pprint

from werkzeug.security import generate_password_hash, check_password_hash

from database import crud, model
from database.model import (
    connect_to_db, db, Cabinet, Category, Concern, Frequency, Ingredient, Interaction, Skintype, Step, Product, ProductIngredient, Routine, User
)
from server import app


ALL_ORMS = [
    Cabinet, Category, Concern, Frequency, Ingredient, Interaction, Skintype, Step,
    Product, ProductIngredient, Routine, User]


def new_set_up():
    print('Running new_set_up now...')
    os.system('dropdb testdb --if-exists')
    os.system('createdb testdb')
    connect_to_db(app, db_uri='postgresql:///testdb', echo=False)
    db.create_all()
    example_data()
    print('Done running new_set_up now...')


def setUp():
    print('Running setUp now...')
    os.system('dropdb testdb --if-exists')
    os.system('createdb testdb')
    connect_to_db(app, db_uri='postgresql:///testdb', echo=False)
    db.create_all()
    example_data()
    print('Done running setUp now...')


def tearDown():
    print('Running tearDown now...')
    db.session.remove()
    db.drop_all()
    db.engine.dispose()
    print('Done running tearDown now...')


def test_setUp_and_tearDown():
    """Test if setUp and tearDown methods are working."""
    # self.assertEqual('a', 'a')
    # self.assertEqual(app.secret_key, 'secret')

# def test_get_user_by_email():
#     test_query = User.query.filter_by(email='email_1@email.com').first()
#     test_user = crud.get_user_by_email('email_1@email.com')
#     self.assertEqual(test_user, test_query)
    
# def test_get_first_obj_by_param():
#     trad_queried_prod = model.User.query.get(1)
#     query_param = {
#         "user_id": 1
#     }
#     crud_queried_prod = crud.get_first_obj_by_param("User", **query_param)
#     self.assertEqual(trad_queried_prod, crud_queried_prod)

# def test_create_user():
#     obj_params = {
#         "email": "sqrpnts@gmail.com",
#         "password": "Pineapple4!",
#         "f_name": "Spongebob",
#         "l_name": "Squarepants"
#     }
#     new_user = crud.create_user(**obj_params)
#     queried_user = crud.get_user_by_email("sqrpnts@gmail.com")
#     self.assertEqual(new_user, queried_user)

def test_create_product_cascade():
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
    # self.assertEqual(new_prod, queried_prod)

def test_create_product_cascade_ingredients():
    """Test object creation cascade for products -> ingredients -> product_ingredients tables.
    SOURCE: https://docs-sqlalchemy.readthedocs.io/ko/latest/orm/cascades.html
    """
    params = {
        "product_name": "Facial Lotion",
        "brand_name": "Aveeno",
        "product_type": "Moisturizer",
        "clean_ingreds": "['ingred1', 'ingred2', 'ingred3', 'ingred4']"
    }
    clean_ingreds_list = crud.convert_string_to_datastructure(params.pop("clean_ingreds"))
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

def test_relationship_skintype_user():
    """Check what Skintype.users returns and vice versa."""
    print('Running test_relationship_skintype_user now...')
    sk1 = Skintype.query.get(1)
    sk1_users = sk1.users
    sk1_ser = sk1.serialize
    print('*' * 20)
    print('Skintype with skintype_id=1 (called sk1) is...')
    print(sk1)
    print('sk1.serialize is...')
    pprint.pprint(sk1_ser)
    print('And sk1.users is...')
    print(sk1_users)
    print('\n')

    user1 = User.query.get(1)
    user1_ser = user1.serialize
    user1_sk = user1.skintype
    print('User with user_id=1 (called user1) is...')
    print(user1)
    print('user1.serialize is...')
    pprint.pprint(user1_ser)
    print('And user1.skintype is...')
    print(user1_sk)
    print('Done running test_relationship_skintype_user now...')


def test_relationship_concern_user():
    """Check what Concern.users returns and vice versa."""
    print('Running test_relationship_concern_user now...')
    con1 = Concern.query.get(1)
    con1_user_concern_1 = con1.user_concern_1
    con1_user_concern_2 = con1.user_concern_2
    con1_ser = con1.serialize
    print('*' * 20)
    print('Concern with concern_id=1 (called con1) is...')
    print(con1)
    print('con1.serialize is...')
    pprint.pprint(con1_ser)
    print('And con1.user_concern_1 is...')
    print(con1_user_concern_1)
    print(con1_user_concern_2)
    print('\n')

    user1 = User.query.get(1)
    user1_ser = user1.serialize
    user1_1con = user1.primary_concern
    user1_2con = user1.secondary_concern
    print('User with user_id=1 (called user1) is...')
    print(user1)
    print('user1.serialize is...')
    pprint.pprint(user1_ser)
    print('And user1.primary_concern is...')
    print(user1_1con)
    print(user1_1con.serialize)
    print('And user1.secondary_concern is...')
    print(user1_2con)
    print(user1_2con.serialize)
    print('Done running test_relationship_concern_user now...')


def example_data():
    """Generate example data for testing purposes."""
    print('Running example_data now...')

    # In case this is run more than once, empty out existing data
    for table in ALL_ORMS:
        table.query.delete()

    # Add sample skintypes and users
    sk1 = Skintype(skintype_name='combination', description='desc1')
    sk2 = Skintype(skintype_name='dry', description='desc2')
    sk3 = Skintype(skintype_name='normal', description='desc3')
    sk4 = Skintype(skintype_name='oily', description='desc4')

    con1 = Concern(concern_name='acne')
    con2 = Concern(concern_name='dryness')
    con3 = Concern(concern_name='redness')
    con4 = Concern(concern_name='wrinkles')

    user1 = User(f_name='Liz', email='email_1@email.com',
        hashed_password=generate_password_hash('pass_1'),
        skintype=sk2, primary_concern=con1, secondary_concern=con4)
    user2 = User(f_name='Nadine', email='email_2@email.com',
        hashed_password=generate_password_hash('pass_2'),
        skintype=sk1, primary_concern=con2)
    user3 = User(f_name='Bob', email='email_3@email.com',
        hashed_password=generate_password_hash('pass_3'),
        skintype=sk3, primary_concern=con2)
    user4 = User(f_name='Jimmy', email='email_4@email.com',
        hashed_password=generate_password_hash('pass_4'),
        skintype=sk1, primary_concern=con3, secondary_concern=con2)
    user5 = User(f_name='Alice', email='email_5@email.com',
        hashed_password=generate_password_hash('pass_5'),
        skintype=sk3, primary_concern=con4)

    cat1 = Category(category_name='Cleanser', description='desc1')
    cat2 = Category(category_name='Moisturizer', description='desc2')

    prod1 = Product(product_name='test_prod1', category=cat1)
    prod2 = Product(product_name='test_prod2', category=cat2)

    db.session.add_all([sk1, sk2, sk3, sk4])
    db.session.add_all([con1, con2, con3, con4])
    db.session.add_all([user1, user2, user3, user4, user5])
    db.session.add(prod1, prod2)
    db.session.commit()
    print('Done running example_data now...')


def test_1026():
    """Test adding a new routine and a single step to that routine.
    Moved from /database/model.py, from where this was originally run."""
    test_user = User.query.first()
    if not test_user:
        test_user = User(f_name='Liz', email='email_1@email.com', hashed_password=generate_password_hash('pass_1'))
        db.session.add(test_user)
        db.session.commit()
    u_id = test_user.user_id
    r1 = Routine(user_id=u_id, am_or_pm='pm')
    s1 = Step()
    db.session.add(r1)
    if Product.query.get(1):
        s1.product_id=1
        r1.steps.append(s1)
    db.session.commit()


if __name__ == "__main__":
    print(db)
    new_set_up()
    print(db)
    test_relationship_skintype_user()
    # terDown()
