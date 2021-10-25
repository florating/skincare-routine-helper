"""CRUD functions for the database."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import ast
from decimal import Decimal
import re
from re import sub

from werkzeug.security import generate_password_hash, check_password_hash

from . import model
from database.model import db, User, Concern, Cabinet, Category, Skintype, SkincareStep, Product, Ingredient, ProductIngredient, Interaction, AMRoutine, PMRoutine, connect_to_db

# REFACTOR-NOTE: consider using __name__ 
FXN_DICT = {
    'Cabinet': Cabinet,
    'Category': Category,
    'Concern': Concern,
    'Ingredient': Ingredient,
    'Interaction': Interaction,
    'Product': Product,
    'ProductIngredient': ProductIngredient,
    'SkincareStep': SkincareStep,
    'Skintype': Skintype,
    'User': User,

    'AMRoutine': AMRoutine,
    'PMRoutine': PMRoutine
}


##### DATABASE INSERTION FUNCTIONS #####

def create_table_obj(table_class_name, **kwargs):
    """Create and return an instance of class table_class_name.
    
    This works best with the table objects that do not have dependencies.
    (eg: db.relationship(...) is never called within these classes.)

    This includes: Concern, Skintype, SkincareStep, Category, Ingredient
    """
    # if 'price' in kwargs:
    #     convert_price(kwargs, kwargs['price'])

    if 'product' == table_class_name.lower():
        # REFACTOR-NOTE: can add to FXN_DICT later
        obj = create_product_cascade(**kwargs)
    else:   
        obj = FXN_DICT[table_class_name](**kwargs)
        add_and_commit(obj)
    return obj


def create_user(**params):
    """Create and return a new User object."""
    # REFACTOR-NOTE: can re-define __init__ method in model.py
    params['hashed_password'] = generate_password_hash(params.pop('password'), method='sha256')  # FIXME: could also salt this
    return create_table_obj('User', **params)


def create_cabinet(u_id, p_id):
    """Create and return a new Cabinet object."""
    obj = Cabinet(user_id=u_id, product_id=p_id)
    add_and_commit(obj)
    return obj


def create_product_cascade(**obj_params):
    """Create and return a new Product object, while also populating the ingredients and product_ingredients tables.
    
    PARAMETERS:
        - obj_params (dict): a dictionary with key-value pairs for class attribute and value
            - eg: obj_params['clean_ingreds'] = "['xanthan gum', 'parfum', 'limonene', 'linalool']" (for example)
    
    OTHER BEHAVIOR:
        If this product does not already exist in the database, then this function also calls create_ingredients_cascade() to populate the ingredients and product_ingredients tables.

    RETURNS:
        - a Product object (if it was inserted into the table)
        - None (if this product already exists in the database)
    """
    # parse product_size out of the product_name field in obj_params
    obj_params = parse_out_product_size(**obj_params)
    # TODO: (TEST THIS!) check if prod_obj.product_name already exists in products table
    if Product.query.filter_by(
        product_name = obj_params['product_name'].rstrip()
        ).all():

        print("This product already exists in the database!")
        return None
        # REFACTOR-NOTE: try using the try/except constructions!
    
    obj_params.pop('ingredients', None)  # toss
    ingreds_list = obj_params.pop('clean_ingreds')
    prod_type = obj_params.pop('product_type', None)

    prod_obj = Product(**obj_params)

    if prod_type:
         cat_obj = Category.query.filter_by(category_name=prod_type).one()
         if cat_obj:
            prod_obj.category_id = cat_obj.category_id
    
    actual_ingreds_list = convert_string_to_list(ingreds_list)
    create_ingredients_cascade(prod_obj, actual_ingreds_list)

    db.session.add(prod_obj)

    # result could be:
    # prod_obj = <Product product_id=2 product_name=Weleda Baby Calendula Cream Bath (200ml) category_id=None>
    # len(ingreds_list) = 200

    db.session.commit()
    print('Session committed!\n\n')
    return prod_obj


def create_ingredients_cascade(product_obj, ingredient_list):
    """Create entries for a list of ingredient names in both the ingredients and product_ingredients tables.
    
    PARAMETERS:
        - product_obj (Product object):
        - ingredient_list (list): a list of strings, referring to the common_names of an Ingredient object

    RETURNS:
        ???
    """

    ingreds_obj_list = []
    proding_obj_list = []
    for i, ing_name in enumerate(ingredient_list):
        # TODO: check if ingredient name is in alternative_name field...
        clean_ing_name = ing_name.rstrip()
        ing_obj = Ingredient.query.filter(Ingredient.common_name.ilike(clean_ing_name)).first()
        if not ing_obj:
            ing_obj = Ingredient(common_name=clean_ing_name)
            ingreds_obj_list.append(ing_obj)
        # check if this product_name was already added to the product_ingredients table for this product!
        # pi_query = ProductIngredient.query.filter_by(common_name=ing_name).first()
        # if pi_query:
        #     continue
        pi_obj = ProductIngredient(abundance_order=(i + 1))
        proding_obj_list.append(pi_obj)
        pi_obj.ingredient = ing_obj
    product_obj.product_ingredients = proding_obj_list
    print(f'Sucessfully added {len(ingreds_obj_list)} ingredient(s) from \n\
        ingredient_list of length {len(ingredient_list)} to the Ingredient table. \n\
        Also simultaneously added {len(ingredient_list)} the ProductIngredient table.\n\
        (Both not yet committed.)')


def add_and_commit(table_obj):
    """Add this object (table_obj) to the database."""
    db.session.add(table_obj)
    db.session.commit()


##### HELPER FUNCTIONS BELOW #####

def parse_out_product_size(**obj_params):
    """Return a dict of parameters in which (1) product_name no longer contains the product_size, and (2) a new key-value pair for product_size now exists in obj_params."""
    first, *middle, last = obj_params['product_name'].rstrip().split()
    digit_in_last = re.search(r'\d', last)
    open_paren_in_last = re.search(r'\(', last)
    close_paren_in_last = re.search(r'\)', last)
    if digit_in_last and logical_xnor(open_paren_in_last, close_paren_in_last):
        obj_params['product_name'] = ' '.join([first] + middle)
        obj_params['product_size'] = last.lstrip('([').rstrip('])')
    return obj_params


def logical_xnor(a, b):
    """Returns true if bool(a) == bool(b)."""
    return bool(a) == bool(b)


def check_if_obj_exists(class_name, param_dict):
    """Return True if object with this key-value pair already exists in the database."""
    class_fxn = FXN_DICT[class_name]
    # was param_key=param_val instead of **param_dict, this might still be wrong...
    obj = class_fxn.query.filter_by(**param_dict).first()
    return bool(obj)


def convert_price(arg_dict, price_key):
    """Convert price to Numeric data type and remove currency symbol.
    This will also remove the price_key from arg_dict.
    Returns modified arg_dict.
    """
    
    price_str = arg_dict[price_key]

    if re.search(r"^(\$|\£)", price_str):
        value = Decimal(sub(r'[^\d.]', '', price_str))
        price_symbol = price_str[:1]

    if price_symbol == '£':
        arg_dict['price_GBP'] = value
        # convert to USD
        # arg_dict['price_USD'] = price_USD
        # FIXME: incomplete!
    elif price_symbol == '$':
        arg_dict['price_USD'] = value

    return arg_dict


def convert_string_to_list(list_str):
    """Convert a list of ingredient names (in string form from a CSV file) into an actual list.
    
    >>> convert_string_to_list("['ingred_1', 'ingred_2', 'ingred_3']")
    ['ingred_1', 'ingred_2', 'ingred_3']
    """
    processed_str = ast.literal_eval(list_str)
    return processed_str


##### QUERY FUNCTIONS BELOW #####

def get_obj_by_id(class_name, obj_id):
    """Return a class_name object (eg: User) by its primary key."""
    return FXN_DICT[class_name].query.get(obj_id)


def get_first_obj_by_param(class_name, **param):
    """Return a class_name object (eg: User) by its expected key-value pair."""
    class_fxn = FXN_DICT[class_name]
    return class_fxn.query.filter_by(**param).first()


def get_user_by_email(email):
    """Return a User object by its email address."""
    return User.query.filter_by(email=email).first()


def get_all_obj(class_name):
    """Return a list of all class_name objects."""
    return db.session.query(class_name).all()


def get_all_obj_by_param(class_name, **param):
    """Return a class_name object (eg: User) by its expected key-value pair."""
    class_fxn = FXN_DICT[class_name]
    return class_fxn.query.filter_by(**param).first()


def get_category_dict():
    """Return a list of category names, ordered by category_id."""
    return {item.category_id: item.category_name for item in Category.query.order_by('category_id').all()}


def count_products_by_category(order_by="category_name"):
    """Count number of products by category_id, returning results as a list of tuples.
    Can order by "category_name" or "category_id".
    EG: [(category_id, category_name, num_products), ...]
    SQL query:
        SELECT c.category_id, c.category_name, COUNT(p.category_id) AS num_products
        FROM products AS p
        INNER JOIN categories AS c ON (p.category_id = c.category_id)
        GROUP BY c.category_id, p.category_id, c.category_name
        ORDER BY c.category_id;
    """
    q = "SELECT c.category_id, c.category_name, COUNT(p.category_id) AS num_products\
        FROM products AS p\
        INNER JOIN categories AS c ON (p.category_id = c.category_id)\
        GROUP BY c.category_id, p.category_id, c.category_name\
        ORDER BY c."
    q += order_by
    print(f"\n\n\n q = {q}")
    cursor = db.session.execute(q)
    result = cursor.fetchall()
    return result


def get_summary_prod_table():
    """Returns summary data for products currently in the database.
    
    each element in the returned list:
        [(category_id, category_name, num_products), avg_num_ingredients]
        [(1, 'Moisturizer', 108), avg_num_ingredients]
    # TODO: ONLY DO THIS WHENEVER THE TABLE CHANGES, AND THEN SAVE THE RESULT!
    """
    results = count_products_by_category()
    summary = []
    for result in results:
        cat_id = result[0]
        summary.append([result, get_avg_num_ingredients_by_category(cat_id)])
    return summary


def get_avg_num_ingredients():
    # results = count_products_by_category
    pass


def get_avg_num_ingredients_by_category(cat_id=1):
    """Returns the average number of ingredients for products with this category_id."""
    prod_list = Product.query.filter_by(category_id=cat_id).all()

    sum_ingreds = 0
    for prod in prod_list:
        sum_ingreds += prod.get_num_ingredients()
    return sum_ingreds / len(prod_list)


if __name__ == '__main__':
    import doctest

    from server import app
    
    doctest.testmod()
    connect_to_db(app)
