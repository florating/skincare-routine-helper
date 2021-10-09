"""Models for the Skincare Routine Helper app."""

from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

print("Hello, I'm in model.py and __name__ = {__name__}!")

db = SQLAlchemy()
db_name = 'project_test'  # change when done with testing

class Concern(db.Model):
    """Create a Concern object for the concerns table."""

    __tablename__ = 'concerns'

    concern_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    concern_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # user_concern_1 = list of User objects with this concern listed as their primary concern
    # user_concern_2 = list of User objects with this concern listed as their secondary concern

    def __repr__(self):
        return f"<Concern concern_id={self.concern_id} concern_name={self.concern_name}>"


class Skintype(db.Model):
    """Create a Skintype object for the skintypes table."""

    __tablename__ = 'skintypes'

    skintype_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skintype_name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # users = list of User objects with this skintype

    def __repr__(self):
        return f"<Skintype skintype_id={self.skintype_id} skintype_name={self.skintype_name}>"


class User(db.Model):
    """Create a User object for each app user."""
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    f_name = db.Column(db.String(25))
    l_name = db.Column(db.String(25), nullable=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    
    # change data type?
    hashed_password = db.Column(db.String(50), nullable=False) 

    # skincare-related:
    skintype_id = db.Column(db.Integer, db.ForeignKey('skintypes.skintype_id'), default='1')  # may need to change default skintype_id
    primary_concern_id = db.Column(db.Integer, db.ForeignKey('concerns.concern_id'), server_default=None)
    secondary_concern_id = db.Column(db.Integer, db.ForeignKey('concerns.concern_id'), server_default=None)

    # If using Twilio API for text notifications:
    # US phone numbers only, in format: '(555) 555-5555'
    # phone_number = db.Column(db.String(14))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    primary_concern = db.relationship('Concern', foreign_keys=[primary_concern_id], backref='user_concern_1')
    secondary_concern = db.relationship('Concern', foreign_keys=[secondary_concern_id], backref='user_concern_2')
    skintype = db.relationship('Skintype', backref='users')
    
    # am_routines = list of AM_Routine objects
    # pm_routines = list of PM_Routine objects
    # cabinets = list of Cabinet objects (associated with skincare Product objects)


    def check_password(self, input_password):
        """Return True if input_password is the correct password."""
        # FIXME: use werkzeug?
        return check_password_hash(self.hashed_password, input_password)


    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class SkincareStep(db.Model):
    """Create a SkincareStep object for the skincare_steps table."""

    __tablename__ = 'skincare_steps'

    step_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    step_name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text, nullable=False)
    # product_type_id = which products are acceptable for this step?
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # am_routines = list of AM_Routine objects, linked to individual steps in the routine
    # pm_routines = list of PM_Routine objects, linked to individual steps in the routine

    def __repr__(self):
        return f"<SkincareStep step_id={self.step_id} step_name={self.step_name}>"


class Category(db.Model):
    """Create a Category object for the categories table.
    
    Categories associated with the Kaggle dataaset include:
        ** Moisturiser
        Serum
        Oil
        Mist
        Balm
        Mask
        Peel
        Eye Care
        Cleanser
        Toner
        Exfoliator
        Bath Salts
        Body Wash
        Bath Oil

    Categories to add:
        Sunscreen
        Essence

    ** = need to change to American English
    """

    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    # products = list of Product objects

    def __repr__(self):
        return f"<Category category_id={self.category_id} category_name={self.category_name}>"


class Product(db.Model):
    """Create a skincare Product object for the products table."""

    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100), nullable=False)
    brand_name = db.Column(db.String(25), nullable=True)
    product_url = db.Column(db.String(100), nullable=True)
    product_size = db.Column(db.String(20), nullable=True)
    price = db.Column(db.String(10), nullable=True)  # convert to Numeric later, and add price conversion into crud.py or here
    price_GBP = db.Column(db.String(10), nullable=True)  # convert to Numeric later, and add price conversion into crud.py or here
    price_USD = db.Column(db.Numeric, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

    # Temporarily created the following 3 fields to handle data from Kaggle dataset. Will map it to Categories
    product_type = db.Column(db.String(20))
    ingredients = db.Column(db.Text)
    clean_ingreds = db.Column(db.Text)

    # specific recommendations per Sephora dataset from jjone36:
    rec_combination = db.Column(db.Boolean, nullable=False, default=False)
    rec_dry = db.Column(db.Boolean, nullable=False, default=False)
    rec_normal = db.Column(db.Boolean, nullable=False, default=False)
    rec_oily = db.Column(db.Boolean, nullable=False, default=False)
    rec_sensitive = db.Column(db.Boolean, nullable=False, default=False)
    
    # other fields that could be added:
    fragrance_free = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    category = db.relationship('Category', backref='products')
    # cabinets = list of Cabinet objects (associated with skincare Product objects)
    # am_routines = list of AM_Routine objects
    # pm_routines = list of PM_Routine objects
    product_ingredients = db.relationship('ProductIngredient', back_populates='products')


    def __repr__(self):
        return f"<Product product_id={self.product_id} product_name={self.product_name} category_id={self.category_id}>"


class Cabinet(db.Model):
    """Create a Cabinet object for the cabinets table."""

    __tablename__ = 'cabinets'

    cabinet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    status = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    users = db.relationship('User', backref='cabinets')
    products = db.relationship('Product', backref='cabinets')

    def __repr__(self):
        return f"<Cabinet cabinet_id={self.cabinet_id} user_id={self.user_id} status={self.status}>"


class Ingredient(db.Model):
    """Create an Ingredient object for the master ingredients table."""

    __tablename__ = 'ingredients'

    ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    common_name = db.Column(db.String(50), nullable=False)
    alternative_name = db.Column(db.String(50), nullable=True)

    active_type = db.Column(db.String(25), nullable=True, server_default=None)
    pm_only = db.Column(db.Boolean, default=False)
    irritation_rating = db.Column(db.Integer)
    endocrine_disruption = db.Column(db.Boolean, default=False)
    carcinogenic = db.Column(db.Boolean, default=False)
    pregnancy_safe = db.Column(db.Boolean, default=False)
    reef_safe = db.Column(db.Boolean, default=False)
    has_fragrance = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    # interactions1 = list of Interaction objects (adverse reactions)
    # interactions2 = list of Interaction objects (adverse reactions)
    product_ingredients = db.relationship('ProductIngredient', back_populates='ingredients')

    def __repr__(self):
        return f"<Ingredient ingredient_id={self.ingredient_id} ingredient_name={self.ingredient_name} active_type={self.active_type}>"


class Interaction(db.Model):
    """Create an Ingredient object for the master interactions table."""

    __tablename__ = 'interactions'

    interaction_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'))
    second_ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'))
    reaction_description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    ingredient1 = db.relationship('Ingredient', foreign_keys=[first_ingredient_id], backref='interactions1')
    ingredient2 = db.relationship('Ingredient', foreign_keys=[second_ingredient_id], backref='interactions2')

    def __repr__(self):
        return f"<Interaction interaction_id={self.interaction_id} first_ingredient_id={self.first_ingredient_id} second_ingredient_id={self.second_ingredient_id}>"


class ProductIngredient(db.Model):
    """Create a ProductIngredient object for the product_ingredients table."""

    __tablename__ = 'product_ingredients'

    prod_ing_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=True)
    ingredient_id = db.Column(db.Integer, db.ForeignKey('ingredients.ingredient_id'), nullable=True)
    abundance_order = db.Column(db.Integer)  # auto-increment, but restart at 1 for new product_id
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    ingredients = db.relationship('Ingredient', back_populates='product_ingredients')
    products = db.relationship('Product', back_populates='product_ingredients')

    def __repr__(self):
        return f"<ProductIngredient prod_ing_id={self.prod_ing_id} product_id={self.product_id} ingredient_id={self.ingredient_id} abundance_order={self.abundance_order}>"


class AMRoutine(db.Model):
    """Create a AMRoutine object for the am_routines table."""

    __tablename__ = 'am_routines'

    routine_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('skincare_steps.step_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=True)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    
    users = db.relationship('User', backref='am_routines')
    products = db.relationship('Product', backref='am_routines')
    steps = db.relationship('SkincareStep', backref='am_routines')

    def __repr__(self):
        return f"<AMRoutine routine_id={self.routine_id} step_id={self.step_id} product_id={self.product_id} status={self.status}>"
    
    def retire(self):
        """Remove product from current routine."""
        self.status = False
    

class PMRoutine(db.Model):
    """Create a PMRoutine object for the pm_routines table."""
    # can this inherit from the AMRoutine class?

    __tablename__ = 'pm_routines'

    routine_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('skincare_steps.step_id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'), nullable=True)
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    users = db.relationship('User', backref='pm_routines')
    products = db.relationship('Product', backref='pm_routines')
    steps = db.relationship('SkincareStep', backref='pm_routines')

    def __repr__(self):
        return f"<PMRoutine routine_id={self.routine_id} step_id={self.step_id} product_id={self.product_id} status={self.status}>"


def connect_to_db(flask_app, db_uri=f"postgresql:///{db_name}", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == '__main__':
    print("Hello, I'm in model.py's special statement since __name__ == '__main__'!")
    import os
    os.system('dropdb project_test --if-exists')
    os.system('createdb project_test')

    from flask import Flask
    app = Flask(__name__)

    connect_to_db(app)
    db.create_all()    
