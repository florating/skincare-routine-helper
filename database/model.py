"""Models for the database."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
import pytz
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, Text
# from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash

# from database.crud import add_and_commit
if sys.version_info[0] >= 3:
    unicode = str
db = SQLAlchemy()
# _db_name_ = 'project_test'  # NOTE: from schema prior to 10/25
_DB_NAME_ = 'project_test_2'  # TODO: change when done with testing
_ECHO_LOG_ERRORS_ = True  # TODO: Change when done with testing

##### TIME-RELATED FUNCTIONS BELOW #####

def get_current_datetime():
    """Return current datetime as an aware datetime object with a UTC timezone."""
    # ISO 8601 format (aware): '2016-11-16T22:31:18.130822+00:00'
    # current_dt = datetime.utcnow().isoformat()

    # current_dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # looks like: '1984-01-10 23:30:00'
    # current_dt = datetime.now().isoformat()  # ISO 8601 format (naive): '1984-01-10T23:30:00'

    return datetime.utcnow()


def convert_to_PST(aware_datetime):
    """Return a converted version of this aware datetime object (UTC --> PST)."""
    # TODO: check if this converts to PST (with daylight saving time status) or just PT
    return aware_datetime.astimezone(pytz.timezone("America/Los_Angeles"))


##### MIXINS BELOW #####

class TimestampMixin(object):
    """Add timestamps for ORM classes."""
    created_on = Column(
        DateTime, nullable=False, default=get_current_datetime())
    updated_on = Column(
        DateTime, nullable=True, default=None, onupdate=get_current_datetime())


class RetiredMixin(TimestampMixin):
    """Add timestamp when this object was retired."""
    retired_on = Column(DateTime, nullable=True, default=None)

    def retire(self):
        """Change retired."""
        self.retired_on = get_current_datetime()


##### TABLES BELOW #####

class Concern(db.Model):
    """Create a Concern object for the concerns table."""

    __tablename__ = 'concerns'

    concern_id = Column(Integer, primary_key=True, autoincrement=True)
    concern_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, default=get_current_datetime())
    
    # user_concern_1 = list of User objects with this concern listed as their primary concern
    # user_concern_2 = list of User objects with this concern listed as their secondary concern

    def __repr__(self):
        return f"<Concern concern_id={self.concern_id} concern_name={self.concern_name}>"


class Skintype(db.Model):
    """Create a Skintype object for the skintypes table."""

    __tablename__ = 'skintypes'

    skintype_id = Column(Integer, primary_key=True, autoincrement=True)
    skintype_name = Column(String(25), nullable=False)
    description = Column(Text, nullable=True)
    created_on = Column(DateTime, default=get_current_datetime())
    
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
    skintype_id = Column(Integer, db.ForeignKey('skintypes.skintype_id'), server_default=None)
    primary_concern_id = Column(Integer, db.ForeignKey('concerns.concern_id'), server_default=None)
    secondary_concern_id = Column(Integer, db.ForeignKey('concerns.concern_id'), server_default=None)

    # If using Twilio API for text notifications:
    # US phone numbers only, in format: '(555) 555-5555'
    # phone_number = db.Column(db.String(14))
    created_on = Column(DateTime, default=get_current_datetime())
    updated_on = Column(
        DateTime, nullable=True, default=None, onupdate=get_current_datetime())

    primary_concern = db.relationship('Concern', foreign_keys=[primary_concern_id], backref='user_concern_1')
    secondary_concern = db.relationship('Concern', foreign_keys=[secondary_concern_id], backref='user_concern_2')
    skintype = db.relationship('Skintype', backref='users')
    
    # perm_user_settings = [user_id, created_on]
    # display_fields = [f_name, l_name, email]
    # skin_display_fields = [skintype, primary_concern, secondary_concern]
    # modifiable_user_settings = [f_name, l_name, email]

    # routines = list of Routine objects
    # cabinets = list of Cabinet objects (associated with skincare Product objects)

    @property
    def serialize(self):
        return {
            'user_id': self.user_id,
            'skintype_id': self.skintype_id,
            'primary_concern_id': self.primary_concern_id,
            'secondary_concern_id': self.secondary_concern_id,
            'cabinets': self.serialize_cabinets,
            'routines': self.serialize_routines,
        }
    @property
    def serialize_cabinets(self):
        return [ item.serialize for item in self.cabinets ]
    @property
    def serialize_cabinet_prod_ids(self):
        return [ item.product_id for item in self.cabinets ]
    @property
    def serialize_routines(self):
        return [ item.serialize for item in self.routines ]

    def get_id(self):
        """Returns a unicode that uniquely identifies this user, and can be used to load the user from the user_loader callback function."""
        return unicode(self.user_id)

    def check_password(self, input_password):
        """Return True if input_password is the correct password."""
        return check_password_hash(self.hashed_password, input_password)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Step(db.Model):
    """Create a SkincareStep object for the skincare_steps table."""

    __tablename__ = 'steps'

    step_id = Column(Integer, primary_key=True, autoincrement=True)
    routine_id = Column(Integer, db.ForeignKey('routines.routine_id'))
    # category_id = Column(Integer, db.ForeignKey('categories.category_id'))
    cardinal_order = Column(Integer, nullable=True, default=None)
    product_id = Column(Integer, db.ForeignKey('products.product_id'), nullable=True)
    interval = Column(Integer, nullable=False, default=1)  # in days
    # FIXME: will need to change this for exfoliants and other actives
    # or for people with sensitive skin, or for beginner routines
    
    notes = Column(Text, nullable=False, default=None)
    created_on = Column(DateTime, default=get_current_datetime())
    updated_on = Column(
        DateTime, nullable=True, default=None, onupdate=get_current_datetime())
    retired_on = Column(DateTime, nullable=True, default=None)
    
    product = db.relationship('Product', backref='steps')
    
    # dates = (list of) Frequency object(s), for usage timestamps
    # routine = Routine objects, linked to individual steps in the routine

    @property
    def serialize(self, verbose=False):
        attributes = {}
        if verbose:
            attributes = {
                'routine_id': self.routine_id,
                'routine_nickname': self.routine.name,
                'am_or_pm': self.routine.am_or_pm,  # can see this from Routine.serialize also
                'product_id': self.product_id,
                'product_name': self.product_name,
                'category_id': self.product.category_id,
                'updated_on': self.updated_on,
                # 'updated_on_PT': convert_to_PST(self.updated_on)  # need to test
            }
        attributes.update({
            'cardinal_order': self.cardinal_order,
            'dates': self.serialize_frequencies,
            'is_retired': bool(self.retired_on)
        })
        return attributes
    @property
    def serialize_dates_only(self, convert_to_PT=False):
        if convert_to_PT:
            return [ convert_to_PST(item.created_on) for item in self.dates ]
        return [ item.created_on for item in self.dates ]
    @property
    def serialize_frequencies(self):
        return [ item.serialize for item in self.dates ]

    def use_product(self, timestamp=get_current_datetime(), notes=None):
        new_freq = Frequency(created_on=timestamp, notes=notes)
        self.dates.append(new_freq)
        # db.session.add(self)  # is this needed to update this row? use new_freq instead of self?
        db.session.commit()

    def change_product(self, keep_notes=False):
        """Change product used for this step (eg: change to a different cleanser)."""
        self.retire()
        new_step = Step(
            routine_id = self.routine_id,
            cardinal_order = self.cardinal_order
        )
        if keep_notes:
            new_step['notes'] = self.notes
        new_step.product = self.product
        db.session.add(new_step)
        db.session.commit()

    def retire(self):
        """Do not use this step anymore."""
        self.retired_on = get_current_datetime()
        db.session.commit()

    def un_retire(self):
        """"""
        new_step = Step(routine_id = self.routine_id)
        # FIXME: need to update cardinal_order... maybe add update_cardinality() to Routine
        db.session.add(new_step)
        db.session.commit()
    
    def __repr__(self):
        return f"<Step step_id={self.step_id} product_id={self.product_id}>"


class Frequency(db.Model):
    """Create a Frequency object to track frequency of use of each skincare step.
    Each Step object is linked to multiple Frequency objects to record:
        - timestamps for dates of use
        - notes (user feedback for themselves)
    """
    freq_id = Column(Integer, primary_key=True, autoincrement=True)
    step_id = Column(Integer, db.ForeignKey('steps.step_id'), nullable=False)
    created_on = Column(DateTime, default=get_current_datetime())
    notes = Column(Text, default=None)
    # NOTE: ALTERNATIVE WAY TO DO THIS...
        # save dates as Array of DateTimes? Or a long string that can be
        # de-string-ified to get dates out of it? Use for data visualization...
            # eg: dates = Column(Text, default=None)

    step = db.relationship('Step', backref='dates')

    @property
    def serialize(self, verbose=False):
        attributes = {}
        if verbose:
            attributes = { 'freq_id': self.freq_id }
        attributes.update({
            'date': self.created_on,
            'notes': self.notes
        })
        return attributes
    
    def __repr__(self):
        return f"<Frequency freq_id={self.freq_id} step_name={self.step_name}>"


class Category(db.Model):
    """Create a Category object for the categories table.
    
    Categories associated with the Kaggle dataset (by difficulty level) include:
        1) Beginner level:
            Cleanser
        Moisturizer
            Sunscreen (will add later)
        2) Intermediate level:
            Toner
        Serum
            Essence (may add later)
            Exfoliator
        Mask
        3) Advanced level:
        Peel
        Eye Care
        99) Miscellaneous:
            Balm
            Bath Oil
        Bath Salts
        Body Wash
            Mist
            Oil
    """

    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(25), nullable=False)
    difficulty_lv = Column(Integer)
    description = Column(Text, nullable=False)
    created_on = Column(DateTime, default=get_current_datetime())
    
    # products = list of Product objects
    
    @property
    def serialize(self):
        return {
            'category_id': self.category_id,
            'category_name': self.category_name,
            'difficulty_lv': self.difficulty_lv
        }

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

    # FIXME: convert to Numeric later, and test price conversion fxn in crud.py
    # price = Column(String(10), nullable=True)
    # price_GBP = Column(String(10), nullable=True)
    # price_USD = Column(Numeric, nullable=True)
    category_id = Column(Integer, db.ForeignKey('categories.category_id'))

    # specific recommendations per Sephora dataset from jjone36:
    # rec_combination = Column(Boolean, nullable=True, default=None)
    # rec_dry = Column(Boolean, nullable=True, default=None)
    # rec_normal = Column(Boolean, nullable=True, default=None)
    # rec_oily = Column(Boolean, nullable=True, default=None)
    # rec_sensitive = Column(Boolean, nullable=True, default=None)
    
    # other fields that could be added:
    # fragrance_free = Column(Boolean, default=None)
    created_on = Column(DateTime, default=get_current_datetime())
    updated_on = Column(
        DateTime, nullable=True, default=None, onupdate=get_current_datetime())
    retired_on = Column(DateTime, nullable=True, default=None)
    
    category = db.relationship('Category', backref='products')
    # cabinets = list of Cabinet objects (associated with this product)
    # steps = list of skincare Step objects
    product_ingredients = db.relationship('ProductIngredient', back_populates='product')

    @property
    def serialize(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category.serialize
        }

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
    created_on = Column(DateTime, default=get_current_datetime())
    retired_on = Column(DateTime, nullable=True, default=None)
    notes = Column(Text, nullable=True, default=None)
    
    user = db.relationship('User', backref='cabinets')
    product = db.relationship('Product', backref='cabinets')

    @property
    def serialize(self):
        return {
            'cabinet_id': self.cabinet_id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'product_name': self.product.product_name,
            'category_id': self.product.category_id
        }
    
    def __repr__(self):
        return f"<Cabinet cabinet_id={self.cabinet_id} user_id={self.user_id} product_id={self.product_id}>"


class Ingredient(db.Model):
    """Create an Ingredient object for the master ingredients table."""

    __tablename__ = 'ingredients'

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    CAS_id = Column(String(12), nullable=True, default=None, unique=True)
    # EXAMPLE: titanium dioxide has a CAS_id of 13463-67-7
    # FORMAT: up to 10 digits, separated by up to 2 hyphens
    # NOTE: how to handle multiple CAS_id values for the same common_name?

    INCI_code = Column(String(50), nullable=True, default=None)
    # NOTE: unique?

    common_name = Column(String(100), nullable=False)
    alternative_names = Column(Text, nullable=True)
    # NOTE: may use to store a list in string form --> "['name_a', 'name_b']"

    active_type = Column(String(50), default=None)
    is_emollient = Column(Boolean, default=None)
    is_humectant = Column(Boolean, default=None)
    is_occlusive = Column(Boolean, default=None)
    pm_only = Column(Boolean, default=None)
    irritation_rating = Column(Integer, default=None)
    endocrine_disruption = Column(Boolean, default=None)

    # CARCINOGENIC INFO
    carcinogenic = Column(Boolean, default=None)
    IARC_group_id = Column(String(2), default=None)  # TODO: create IARC table (3 rows)

    # pregnancy_safe = Column(Boolean, default=None)
    # reef_safe = Column(Boolean, default=None)
    is_fragrance = Column(Boolean, default=None)
    created_on = Column(DateTime, default=get_current_datetime())

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # FIXME: add more later
        fragrances = {'parfum', 'perfume', 'fragrance', 'aroma', 'essential oil blend'}
        if self.common_name.lower() in fragrances:
            self.is_fragrance = True 

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
    created_on = Column(DateTime, default=get_current_datetime())

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
    created_on = Column(DateTime, default=get_current_datetime())
    
    ingredient = db.relationship('Ingredient', back_populates='product_ingredients')
    product = db.relationship('Product', back_populates='product_ingredients')

    def __repr__(self):
        return f"<ProductIngredient prod_ing_id={self.prod_ing_id} product_id={self.product_id} ingredient_id={self.ingredient_id} abundance_order={self.abundance_order}>"
    

class Routine(db.Model):
    """Create a Routine object for the routines table."""

    __tablename__ = 'routines'

    routine_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.user_id'), nullable=False)
    am_or_pm = Column(String(2), nullable=False)
    name = Column(String(25))
    # step_id = Column(Integer, db.ForeignKey('steps.step_id'), nullable=False)
    created_on = Column(DateTime, default=get_current_datetime())
    updated_on = Column(DateTime, nullable=True, default=None, onupdate=get_current_datetime())
    retired_on = Column(DateTime, nullable=True, default=None)

    user = db.relationship('User', backref='routines')
    steps = db.relationship('Step', backref='routine')

    @property
    def serialize(self):
        return {
            'routine_id': self.routine_id,
            'user_id': self.user_id,
            'name': self.name,
            'am_or_pm': self.am_or_pm,
            # 'product_name': self.product_name,
            # 'category_id': self.product.category_id
        }
    @property
    def serialize_current_steps(self, verbose=False):
        if verbose:
            return [ item.serialize for item in self.steps if not bool(item.retired_on) ]
        return [ [ item.step_id, item.product_id ] for item in self.steps if not bool(item.retired_on) ]
    
    # def update_cardinality(self):
    #     """Save the order in which skincare steps are performed."""
    #     for step in self.steps:
    #         step.cardinal_order = something
    #     db.session.commit()

    def __repr__(self):
        return f"<Routine routine_id={self.routine_id} name={self.name} user_id={self.user_id} am_or_pm={self.am_or_pm} number of steps={len(self.steps) if self.steps else None}>"


##### DB-RELATED FUNCTION BELOW #####

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

    connect_to_db(flask_app=app, db_uri=f"postgresql:///{_DB_NAME_}", echo=False)
    db.create_all()
