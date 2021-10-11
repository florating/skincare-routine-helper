import ast
from decimal import Decimal
import re
from re import sub

from werkzeug.security import generate_password_hash, check_password_hash

from model import db, User, Concern, Cabinet, Category, Skintype, SkincareStep, Product, Ingredient, ProductIngredient, Ingredient, Interaction, AMRoutine, PMRoutine, connect_to_db


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
        obj = create_product_cascade(**kwargs)
    else:   
        obj = FXN_DICT[table_class_name](**kwargs)
        add_and_commit(obj)
    return obj


def create_user(**params):
    """Create and return a new User object."""
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
    
    If this product does not already exist in the database, then this function also calls create_ingredients_cascade() to populate the ingredients and product_ingredients tables.

    RETURNS:
        - a Product object (if it was inserted into the table)
        - None (if this product already exists in the database)
    """

    obj_params.pop('ingredients', None)  # toss
    prod_type = obj_params.pop('product_type', None)
    if prod_type is not None:
         cat_obj = Category.query.filter(Category.category_name == prod_type).first()
         if cat_obj is not None:
            obj_params['category_id'] = cat_obj.category_id
    ingreds_list = obj_params.pop('clean_ingreds')

    prod_obj = Product(**obj_params)

    # FIXME: check if prod_obj.product_name already exists in products table
    # if Product.query.filter(Product.product_name == prod_obj.product_name).all():
    db.session.add(prod_obj)
    db.session.flush()

    # result could be:
    # prod_obj = <Product product_id=2 product_name=Weleda Baby Calendula Cream Bath (200ml) category_id=None>
    # len(ingreds_list) = 200

    actual_ingreds_list = convert_string_to_list(ingreds_list)
    create_ingredients_cascade(prod_obj, actual_ingreds_list)
    db.session.commit()
    print('Session committed!\n\n')
    return prod_obj
    # else:
    #     print('Product with this name already exists in the database.')
    #     return None


def create_ingredients_cascade(product_obj, ingredient_list):
    """Create entries for a list of ingredient names in both the ingredients and product_ingredients tables.
    
    PARAMETERS:
        - product_obj (Product object):
        - ingredient_list (list): a list of strings, referring to the common_names of an Ingredient object

    RETURNS:
        ???
    """

    p_id = product_obj.product_id
    created_ing_objs = []
    for i, ing_name in enumerate(ingredient_list):
        ing_obj = Ingredient.query.filter(Ingredient.common_name == ing_name).first()
        if ing_obj is None:
            ing_obj = create_ingredient(ing_name)
            created_ing_objs.append(ing_obj)
        create_product_ingredient(p_id, ing_obj, i + 1)
    print(f'Sucessfully added {len(created_ing_objs)} ingredient(s) from \n\
        ingredient_list of length {len(ingredient_list)} to the Ingredient table. \n\
        Also simultaneously added {len(ingredient_list)} the ProductIngredient table.\n\
        (Both not yet committed.)')


def create_ingredient(name, alt_name=None):
    """Create and return a new Ingredient object."""
    obj = Ingredient(
        common_name=name,
        alternative_name=alt_name)
    db.session.add(obj)
    return obj


def create_product_ingredient(p_id, ing_obj, abundance_order):
    """Create and return a new ProductIngredient object."""
    obj = ProductIngredient(
        product_id=p_id, 
        ingredient_id=ing_obj.ingredient_id, 
        abundance_order=abundance_order)
    db.session.add(obj)
    return obj


def add_and_commit(table_obj):
    """Add this object (table_obj) to the database."""
    db.session.add(table_obj)
    db.session.commit()


##### HELPER FUNCTIONS BELOW #####

def check_if_obj_exists(class_name, param_key, param_val):
    """Return True if object with this key-value pair already exists in the database."""
    class_fxn = FXN_DICT[class_name]
    obj = class_fxn.query.filter_by(param_key=param_val).first()
    return not not obj


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
    
    >>> convert_string_to_list('['ingred_1', 'ingred_2', 'ingred_3']')
    ['ingred_1', 'ingred_2', 'ingred_3']
    """
    processed_str = ast.literal_eval(list_str)
    return processed_str


##### QUERY FUNCTIONS BELOW #####

def get_obj_by_id(class_name, obj_id):
    """Return a class_name object (eg: User) by its id."""
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


if __name__ == '__main__':
    import doctest

    from server import app
    
    doctest.testmod()
    connect_to_db(app)
