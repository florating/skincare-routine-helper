from model import db, User, Concern, Cabinet, Category, Skintype, SkincareStep, Product, Ingredient, ProductIngredient, Ingredient, Interaction, AMRoutine, PMRoutine, connect_to_db
import ast


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

# These table objects do not have dependencies.


def create_table_obj(table_class_name, **kwargs):
    """Create and return an instance of class table_class_name.
    
    This works best with the table objects that do not have dependencies.
    (eg: db.relationship(...) is never called within these classes.)

    This includes: Concern, Skintype, SkincareStep, Category, Ingredient
    """
    # if 'price' in kwargs:
    #     convert_price(kwargs, kwargs['price'])

    if 'product' == table_class_name.lower():
        obj = create_product_cascade(table_class_name, **kwargs)
        
        # Start adding ingredients to ingredients and product_ingredients tables:
        # product_id = db.session.query(Product.product_id).count()
        # for i, ingred in enumerate(ingreds):
        #     ingred_obj = create_ingredient(ingred)
        #     create_product_ingredient(p_id=product_id, ing_obj=ingred_obj, abundance_order=(i + 1))
    else:   
        obj = FXN_DICT[table_class_name](**kwargs)
        add_and_commit(obj)
    return obj


# def convert_price(arg_dict, price_key):
#     """Convert price to Numeric data type and remove currency symbol.
#     This will also remove the price_key from arg_dict.
#     Returns modified arg_dict.
#     """
#     price_str = arg_dict[price_key]
#     # Convert price to USD if BP and vice versa
#     # FIXME: incomplete!
#     return arg_dict


def create_user(**kwargs):
    """Create and return a new User object."""
    print("Work in progress!")


def create_cabinet(u_id, p_id):
    """Create and return a new Cabinet object."""
    obj = Cabinet(user_id=u_id, product_id=p_id)
    add_and_commit(obj)
    return obj


def create_product_cascade(table_class_name, **kwargs):
    """Create and return a new Product object, while also populating the ingredients and product_ingredients tables."""

    kwargs.pop('ingredients', None)  # toss
    ingreds_list = kwargs.pop('clean_ingreds')
    prod_obj = FXN_DICT[table_class_name](**kwargs)
    db.session.add(prod_obj)
    db.session.flush()
    print(f'prod_obj={prod_obj}, len(ingreds_list)={len(ingreds_list)}')
    print('\n\n')
    print(f'ingreds_list = {ingreds_list}')
    print('\n\n')
    # result was:
    # prod_obj=<Product product_id=2 product_name=Weleda Baby Calendula Cream Bath (200ml) category_id=None>, len(ingreds_list)=200
    actual_ingreds_list = convert_string_to_list(ingreds_list)

    # When I'm feeling brave, I can use product_id to start adding ingredients to the ingredients and product_ingredients tables!
    create_ingredients_cascade(prod_obj, actual_ingreds_list)

    db.session.commit()
    return prod_obj


def convert_string_to_list(list_str):
    """Convert a list of ingredient names (in string form from a CSV file) into an actual list."""
    # list_str = ingreds_list = ['prunus amygdalus dulcis', 'sesamium indicum seed oil', 'alcohol', 'glycerin', 'glyceryl oleate', 'calendula officinalis extract', 'sodium cera alba', 'xanthan gum', 'parfum', 'limonene', 'linalool']
    processed_str = ast.literal_eval(list_str)
    return processed_str


def create_ingredients_cascade(product_obj, ingredient_list):
    """Create entries for a list of ingredient names in both the ingredients and product_ingredients tables.
    
    PARAMETERS:
        - product_obj (Product object):
        - ingredient_list (list): a list of strings, referring to the common_names of an Ingredient object

    RETURNS:
        ???
    """

    p_id = product_obj.product_id
    for i, ing_name in enumerate(ingredient_list):
        ing_obj = create_ingredient(ing_name)
        create_product_ingredient(p_id, ing_obj, i + 1)


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


if __name__ == '__main__':
    from model import app
    connect_to_db(app)