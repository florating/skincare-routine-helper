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

def create_user(**kwargs):
    """Create and return a new User object."""
    print("Work in progress!")


def create_category(name, desc):
    """Create and return a new Category object."""
    categ = Category(category_name=name, description=desc)
    add_and_commit(categ)
    return categ


def create_table_obj(table_class_name, **kwargs):
    """Create and return an instance of class table_class_name."""
    # if 'price' in kwargs:
    #     convert_price(kwargs, kwargs['price'])
    if 'product' == table_class_name.lower():
        kwargs.pop('ingredients')  # toss
        ingreds = kwargs.pop('clean_ingreds')
        obj = FXN_DICT[table_class_name.title()](**kwargs)
        add_and_commit(obj)
        
        # Start adding ingredients to ingredients and product_ingredients tables:
        # product_id = db.session.query(Product.product_id).count()
        # for i, ingred in enumerate(ingreds):
        #     ingred_obj = create_ingredient(ingred)
        #     create_product_ingredient(p_id=product_id, ing_obj=ingred_obj, abundance_order=(i + 1))
    else:   
        obj = FXN_DICT[table_class_name.title()](**kwargs)
        add_and_commit(obj)
    return obj


def convert_price(arg_dict, price_key):
    """Convert price to Numeric data type and remove currency symbol.
    This will also remove the price_key from arg_dict.
    Returns modified arg_dict.
    """
    price_str = arg_dict[price_key]
    # Convert price to USD if BP and vice versa
    # FIXME: incomplete!
    return arg_dict

# def create_(**kwargs):
#     """Create and return a new Concern object."""
#     obj = Concern(**kwargs)
#     add_and_commit(obj)
#     return obj


def create_concern(name, desc):
    """Create and return a new Concern object."""
    obj = Concern(concern_name=name, description=desc)
    add_and_commit(obj)
    return obj


def create_skintype(name, desc):
    """Create and return a new Skintype object."""
    obj = Skintype(skintype_name=name, description=desc)
    add_and_commit(obj)
    return obj


def create_skincarestep(name, desc):
    """Create and return a new SkincareStep object."""
    obj = SkincareStep(step_name=name, description=desc)
    add_and_commit(obj)
    return obj


def create_cabinet(u_id, p_id):
    """Create and return a new Cabinet object."""
    obj = Cabinet(user_id=u_id, product_id=p_id)
    add_and_commit(obj)
    return obj


def create_product(name, brand, cat_name, url=None, product_size=None, price_GBP=None, price_USD=None):
    """Create and return a new Product object."""
    cat_id = db.session.query(Category).filter(Category.category_name == cat_name).first().category_id
    obj = Product(
        product_name=name,
        brand_name=brand,
        url=url,
        product_size=product_size,
        price_GBP=price_GBP,
        price_USD=price_USD,
        category_id=cat_id)
    add_and_commit(obj)
    return obj


def create_ingredient(name, alt_name=None):
    """Create and return a new Ingredient object."""
    obj = Ingredient(
        common_name=name,
        alternative_name=alt_name)
    add_and_commit(obj)
    return obj


def create_product_ingredient(p_id, ing_obj, abundance_order):
    """Create and return a new ProductIngredient object."""
    obj = ProductIngredient(
        product_id=p_id, 
        ingredient_id=ing_obj.ingredient_id, 
        abundance_order=abundance_order)
    add_and_commit(obj)
    return obj


def add_and_commit(table_obj):
    """Add this object (table_obj) to the database."""
    db.session.add(table_obj)
    db.session.commit()


if __name__ == '__main__':
    from server import app
    connect_to_db(app)