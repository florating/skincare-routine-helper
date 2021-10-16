"""Models for the Skincare Routine Helper app."""

from datetime import datetime, timezone

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

print(f"Hello, I'm in model.py and __name__ = {__name__}!")

db = SQLAlchemy()
_db_name = 'project_test'  # FIXME: change when done with testing


class TimestampMixin(object):
    created_at = Column(DateTime, nullable=False, default=datetime.now(timezone.utc))
    updated = Column(DateTime, onupdate=datetime.now(timezone.utc))


class Concern(db.Model):
    """Create a Concern object for the concerns table."""

    __tablename__ = 'concerns'

    concern_id = Column(Integer, primary_key=True, autoincrement=True)
    concern_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # user_concern_1 = list of User objects with this concern listed as their primary concern
    # user_concern_2 = list of User objects with this concern listed as their secondary concern

    def __repr__(self):
        return f"<Concern concern_id={self.concern_id} concern_name={self.concern_name}>"


class Skintype(db.Model):
    """Create a Skintype object for the skintypes table."""

    __tablename__ = 'skintypes'

    skintype_id = Column(Integer, primary_key=True, autoincrement=True)
    skintype_name = Column(String(25), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # users = list of User objects with this skintype

    def __repr__(self):
        return f"<Skintype skintype_id={self.skintype_id} skintype_name={self.skintype_name}>"


class User(UserMixin, db.Model):
    """Create a User object for each app user."""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    f_name = Column(String(25))
    l_name = Column(String(25), nullable=True)
    email = Column(String(50), nullable=False, unique=True)
    
    # FIXME: change data type?
    hashed_password = Column(String(200), nullable=False)

    # skincare-related:
    skintype_id = Column(Integer, db.ForeignKey('skintypes.skintype_id'), default=None)
    primary_concern_id = Column(Integer, db.ForeignKey('concerns.concern_id'), server_default=None)
    secondary_concern_id = Column(Integer, db.ForeignKey('concerns.concern_id'), server_default=None)

    # If using Twilio API for text notifications:
    # US phone numbers only, in format: '(555) 555-5555'
    # phone_number = db.Column(db.String(14))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    primary_concern = db.relationship('Concern', foreign_keys=[primary_concern_id], backref='user_concern_1')
    secondary_concern = db.relationship('Concern', foreign_keys=[secondary_concern_id], backref='user_concern_2')
    skintype = db.relationship('Skintype', backref='users')
    
    perm_user_settings = [user_id, created_at]
    display_fields = [f_name, l_name, email]
    skin_display_fields = [skintype, primary_concern, secondary_concern]
    modifiable_user_settings = [f_name, l_name, email]

    # am_routines = list of AM_Routine objects
    # pm_routines = list of PM_Routine objects
    # cabinets = list of Cabinet objects (associated with skincare Product objects)

    def get_id(self):
        """Returns a unicode that uniquely identifies this user, and can be used to load the user from the user_loader callback function."""
        return str(self.user_id).encode("utf-8").decode("utf-8") 

    # def get(self, unicode_id):
    #     """Reloads the user object from the user ID stored in unicode in the session."""
    #     return User.query.get(unicode_id)

    def check_password(self, input_password):
        """Return True if input_password is the correct password."""
        return check_password_hash(self.hashed_password, input_password)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class SkincareStep(db.Model):
    """Create a SkincareStep object for the skincare_steps table."""

    __tablename__ = 'skincare_steps'

    step_id = Column(Integer, primary_key=True, autoincrement=True)
    step_name = Column(String(25), nullable=False)
    description = Column(Text, nullable=False)
    # product_type_id = which products are acceptable for this step?
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # am_routines = list of AM_Routine objects, linked to individual steps in the routine
    # pm_routines = list of PM_Routine objects, linked to individual steps in the routine

    def __repr__(self):
        return f"<SkincareStep step_id={self.step_id} step_name={self.step_name}>"


class Category(db.Model):
    """Create a Category object for the categories table.
    
    Categories associated with the Kaggle dataaset include:
        Moisturizer
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
    """

    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(25), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # products = list of Product objects

    def __repr__(self):
        return f"<Category category_id={self.category_id} category_name={self.category_name}>"


class Product(db.Model):
    """Create a skincare Product object for the products table."""

    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(200), nullable=False)
    brand_name = Column(String(25), nullable=True)
    product_url = Column(String(200), nullable=True)
    product_size = Column(String(20), nullable=True)
    price = Column(String(10), nullable=True)  # FIXME: convert to Numeric later, and add price conversion into crud.py or here
    # price_GBP = Column(String(10), nullable=True)  # FIXME: convert to Numeric later, and add price conversion into crud.py or here
    price_USD = Column(Numeric, nullable=True)
    category_id = Column(Integer, db.ForeignKey('categories.category_id'))

    # FIXME: Temporarily created the following field to handle data from 
    # Kaggle dataset. Will map it to Categories
    product_type = Column(String(20))

    # specific recommendations per Sephora dataset from jjone36:
    # rec_combination = Column(Boolean, nullable=False, default=False)
    # rec_dry = Column(Boolean, nullable=False, default=False)
    # rec_normal = Column(Boolean, nullable=False, default=False)
    # rec_oily = Column(Boolean, nullable=False, default=False)
    # rec_sensitive = Column(Boolean, nullable=False, default=False)
    
    # other fields that could be added:
    # fragrance_free = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    category = db.relationship('Category', backref='products')
    # cabinets = list of Cabinet objects (associated with this product)
    # am_routines = list of AM_Routine objects
    # pm_routines = list of PM_Routine objects
    product_ingredients = db.relationship('ProductIngredient', back_populates='product')

    def get_num_ingredients(self):
        """Return number of ingredients (besides water) associated with this product."""
        return len(self.product_ingredients)

    def __repr__(self):
        return f"<Product product_id={self.product_id} product_name={self.product_name} category_id={self.category_id}>"


class Cabinet(db.Model):
    """Create a Cabinet object for the cabinets table."""

    __tablename__ = 'cabinets'

    cabinet_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = Column(Integer, db.ForeignKey('products.product_id'))
    # status = Column(Boolean, nullable=False, default=True)  # FIXME: change name
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    users = db.relationship('User', backref='cabinets')
    product = db.relationship('Product', backref='cabinets')

    def __repr__(self):
        # TODO: test that product={...} will show up properly
        return f"<Cabinet cabinet_id={self.cabinet_id} user_id={self.user_id} product={self.product.product_name}>"


class Ingredient(db.Model):
    """Create an Ingredient object for the master ingredients table."""

    __tablename__ = 'ingredients'

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    common_name = Column(String(100), nullable=False)
    alternative_name = Column(Text, nullable=True)

    active_type = Column(String(50), nullable=True, server_default=None)
    pm_only = Column(Boolean, default=False)
    irritation_rating = Column(Integer)
    endocrine_disruption = Column(Boolean, default=False)
    carcinogenic = Column(Boolean, default=False)
    pregnancy_safe = Column(Boolean, default=False)
    reef_safe = Column(Boolean, default=False)
    has_fragrance = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # interactions1 = list of Interaction objects (adverse reactions)
    # interactions2 = list of Interaction objects (adverse reactions)
    product_ingredients = db.relationship('ProductIngredient', back_populates='ingredient')

    def __repr__(self):
        return f"<Ingredient ingredient_id={self.ingredient_id} common_name={self.common_name} active_type={self.active_type}>"


class Interaction(db.Model):
    """Create an Ingredient object for the master interactions table."""

    __tablename__ = 'interactions'

    interaction_id = Column(Integer, primary_key=True, autoincrement=True)
    first_ingredient_id = Column(Integer, db.ForeignKey('ingredients.ingredient_id'))
    second_ingredient_id = Column(Integer, db.ForeignKey('ingredients.ingredient_id'))
    reaction_description = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    ingredient1 = db.relationship('Ingredient', foreign_keys=[first_ingredient_id], backref='interactions1')
    ingredient2 = db.relationship('Ingredient', foreign_keys=[second_ingredient_id], backref='interactions2')

    def __repr__(self):
        return f"<Interaction interaction_id={self.interaction_id} first_ingredient_id={self.first_ingredient_id} second_ingredient_id={self.second_ingredient_id}>"


class ProductIngredient(db.Model):
    """Create a ProductIngredient object for the product_ingredients table."""

    __tablename__ = 'product_ingredients'

    prod_ing_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, db.ForeignKey('products.product_id'), nullable=True)
    ingredient_id = Column(Integer, db.ForeignKey('ingredients.ingredient_id'), nullable=True)    # onUpdate='cascade' ?
    abundance_order = Column(Integer)  # auto-increment, but restart at 1 for new product_id
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    ingredient = db.relationship('Ingredient', back_populates='product_ingredients')
    product = db.relationship('Product', back_populates='product_ingredients')

    def __repr__(self):
        return f"<ProductIngredient prod_ing_id={self.prod_ing_id} product_id={self.product_id} ingredient_id={self.ingredient_id} abundance_order={self.abundance_order}>"


class AMRoutine(db.Model):
    """Create a AMRoutine object for the am_routines table."""

    __tablename__ = 'am_routines'

    routine_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.user_id'), nullable=False)
    step_id = Column(Integer, db.ForeignKey('skincare_steps.step_id'), nullable=False)
    product_id = Column(Integer, db.ForeignKey('products.product_id'), nullable=True)
    # status = Column(Boolean, default=True)    # FIXME: change name
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    users = db.relationship('User', backref='am_routines')
    product = db.relationship('Product', backref='am_routines')
    steps = db.relationship('SkincareStep', backref='am_routines')

    def __repr__(self):
        # TODO: test that product={...} will show up properly
        return f"<AMRoutine routine_id={self.routine_id} step_id={self.step_id} product_id={self.product_id} product={self.product.product_name}>"
    
    def retire(self):
        """Remove product from current routine."""
        self.status = False
    

class PMRoutine(db.Model):
    """Create a PMRoutine object for the pm_routines table."""
    # can this inherit from the AMRoutine class?

    __tablename__ = 'pm_routines'

    routine_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.user_id'), nullable=False)
    step_id = Column(Integer, db.ForeignKey('skincare_steps.step_id'), nullable=False)
    product_id = Column(Integer, db.ForeignKey('products.product_id'), nullable=True)
    # status = Column(Boolean, default=True)    # FIXME: change name
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    users = db.relationship('User', backref='pm_routines')
    product = db.relationship('Product', backref='pm_routines')
    steps = db.relationship('SkincareStep', backref='pm_routines')

    def __repr__(self):
        # TODO: test that product={...} will show up properly
        return f"<PMRoutine routine_id={self.routine_id} step_id={self.step_id} product_id={self.product_id} product={self.product.product_name}>"


def connect_to_db(flask_app, db_uri=f"postgresql:///{_db_name}", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == '__main__':
    print("Hello, I'm in model.py's special statement since __name__ == '__main__'!")

    from server import app

    connect_to_db(app)
    db.create_all()
