"""Models for the database."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pprint

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text
from sqlalchemy.orm import deferred
from werkzeug.security import check_password_hash

from database.model_helpers import convert_to_PST, get_current_datetime, TimestampMixin
# TODO: check if this works before removing those lines of code from this file

if sys.version_info[0] >= 3:
    unicode = str

db = SQLAlchemy()

_ECHO_LOG_ERRORS_ = True  # TODO: Change when done with testing


##### TABLES BELOW #####

class Concern(TimestampMixin, db.Model):
    """Create a Concern object for the concerns table."""

    __tablename__ = 'concerns'

    concern_id = Column(Integer, primary_key=True, autoincrement=True)
    concern_name = Column(String(100), nullable=False)
    description = deferred(Column(Text, nullable=True))
    
    # user_concern_1 = list of User objects with this concern listed as their primary concern
    # user_concern_2 = list of User objects with this concern listed as their secondary concern

    @property
    def serialize(self):
        return {
            'concern_id': self.concern_id,
            'concern_name': self.concern_name,
            'user_concern_1': self.user_concern_1,
            'user_concern_2': self.user_concern_2,
        }
    
    def __repr__(self):
        return f"<Concern concern_id={self.concern_id} concern_name={self.concern_name}>"


class Skintype(TimestampMixin, db.Model):
    """Create a Skintype object for the skintypes table."""

    __tablename__ = 'skintypes'

    skintype_id = Column(Integer, primary_key=True, autoincrement=True)
    skintype_name = Column(String(25), nullable=False)
    description = Column(Text, nullable=True)
    
    # users = list of User objects with this skintype

    @property
    def serialize(self):
        return {
            'skintype_id': self.skintype_id,
            'skintype_name': self.skintype_name,
        }
    
    def __repr__(self):
        return f"<Skintype skintype_id={self.skintype_id} skintype_name={self.skintype_name}>"


class User(TimestampMixin, UserMixin, db.Model):
    """Create a User object for each app user."""
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    f_name = Column(String(25))
    l_name = Column(String(25))
    email = Column(String(50), nullable=False, unique=True)
    hashed_password = deferred(Column(String(200), nullable=False))

    # skincare-related:
    skintype_id = Column(Integer, db.ForeignKey('skintypes.skintype_id'), server_default=None)
    primary_concern_id = Column(Integer, db.ForeignKey('concerns.concern_id'), server_default=None)
    secondary_concern_id = deferred(Column(Integer, db.ForeignKey('concerns.concern_id'), server_default=None))

    primary_concern = db.relationship('Concern', foreign_keys=[primary_concern_id], backref='user_concern_1')
    secondary_concern = db.relationship('Concern', foreign_keys=[secondary_concern_id], backref='user_concern_2')
    skintype = db.relationship('Skintype', backref='users')

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
    def serialize_for_profile(self):
        return {
            'Skin Type': self.skintype.skintype_name if self.skintype_id else '---',
            'Primary Concern': self.primary_concern.concern_name if self.primary_concern_id else '---',
            'Secondary Concern': self.secondary_concern.concern_name if self.secondary_concern_id else '---',
            'Email': self.email,
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
    @property
    def serialize_active_routines(self):
        active_routines = [ item for item in self.routines if item.is_active ]
        am, pm = None, None
        for routine in active_routines:
            if routine.am_or_pm == 'am':
                am = routine
            elif routine.am_or_pm == 'pm':
                pm = routine
        return {
            'am': am,
            'pm': pm,
        }

    def get_id(self):
        """Returns unicode user_id; used for user_loader callback function."""
        return unicode(self.user_id)

    def get_current_routine_id(self, am_or_pm):
        return self.serialize_active_routines.get(am_or_pm)

    def check_password(self, input_password):
        """Return True if input_password is the correct password."""
        return check_password_hash(self.hashed_password, input_password)

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"


class Category(db.Model):
    """Create a Category object for the categories table."""

    __tablename__ = 'categories'

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(25), nullable=False)
    difficulty_lv = Column(Integer)
    description = Column(Text, nullable=True)
    created_on = Column(DateTime, default=get_current_datetime)
    
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


class Product(TimestampMixin, db.Model):
    """Create a skincare Product object for the products table."""

    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(200), nullable=False)
    brand_name = Column(String(25), nullable=True)
    product_url = Column(String(200), nullable=True)
    img_url = deferred(Column(String(200), nullable=True))
    cloud_img_url = deferred(Column(String(200), nullable=True))

    # FIXME: convert to Numeric later, and test price conversion fxn in crud.py
    # price = Column(String(10), nullable=True)
    category_id = Column(Integer, db.ForeignKey('categories.category_id'))

    # specific recommendations per Sephora dataset from jjone36:
    rec_combination = Column(Boolean, nullable=True, default=None)
    rec_dry = Column(Boolean, nullable=True, default=None)
    rec_normal = Column(Boolean, nullable=True, default=None)
    rec_oily = Column(Boolean, nullable=True, default=None)
    rec_sensitive = Column(Boolean, nullable=True, default=None)
    
    # other fields that could be added:
    fragrance_free = Column(Boolean, default=None)

    # TODO: add these fields to model!
    # is_carcinogenic = Column(Boolean, default=None)
    # is_pregnancy_safe = Column(Boolean, default=None)
    # is_environmental_hazard = Column(Boolean, default=None)
    
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
    @property
    def serialize_top_five(self):
        """Return a dict of 0-indexed keys and paired ingredient objects for the top 5 ingredients."""
        return { i: item.ingredient for i, item in enumerate(self.product_ingredients[:5]) }
    @property
    def serialize_top_five_names(self):
        return { item.ingredient.common_name.upper() for item in self.product_ingredients[:5] }
    @property
    def serialize_all_ingreds(self):
        return { item.ingredient.common_name.upper() for item in self.product_ingredients }

    def get_num_ingredients(self):
        return len(self.product_ingredients)

    def get_top_five(self):
        return self.product_ingredients[:5]
    
    def __repr__(self):
        return f"<Product product_id={self.product_id} product_name={self.product_name} category_id={self.category_id}>"


class Cabinet(TimestampMixin, db.Model):
    """Create a Cabinet object for the cabinets table."""

    __tablename__ = 'cabinets'

    cabinet_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.user_id'), nullable=False)
    product_id = Column(Integer, db.ForeignKey('products.product_id'))
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
            'category_id': self.product.category_id,
            'has_notes?': bool(self.notes)
        }
    
    def __repr__(self):
        return f"<Cabinet cabinet_id={self.cabinet_id} user_id={self.user_id} product_id={self.product_id}>"


class Ingredient(TimestampMixin, db.Model):
    """Create an Ingredient object for the master ingredients table."""

    __tablename__ = 'ingredients'

    ingredient_id = Column(Integer, primary_key=True, autoincrement=True)
    INCI_code = Column(String(50), nullable=True, default=None)
    CAS_id = Column(String(12), nullable=True, default=None, unique=True)
    # EXAMPLE: titanium dioxide has a CAS_id of 13463-67-7
    # FORMAT: up to 10 digits, separated by up to 2 hyphens
    # NOTE: how to handle multiple CAS_id values for the same common_name?

    common_name = Column(String(100), nullable=False)
    alternative_names = Column(Text, default=None)
    # NOTE: may use to store a list in string form --> "['name_a', 'name_b']"

    active_type = Column(String(20), default=None)
    hydration_type = Column(String(10), default=None)
    special_type = Column(String(30), default=None)

    is_fragrance = deferred(Column(Boolean, default=None))
    is_formaldehyde = deferred(Column(Boolean, default=None))
    is_sunscreen = Column(Boolean, default=None)
    is_silicone = deferred(Column(Boolean, default=None))
    is_sulfate = deferred(Column(Boolean, default=None))
    is_phthalate = deferred(Column(Boolean, default=None))
    is_paraben = deferred(Column(Boolean, default=None))

    pm_only = Column(Boolean, default=None)
    is_pregnancy_safe = Column(Boolean, default=None)
    irritation_rating = deferred(Column(Boolean, default=None))
    is_endocrine_disruptor = Column(Boolean, default=None)

    # CARCINOGENIC INFO
    is_carcinogenic = Column(Boolean, default=None)
    IARC_group_id = deferred(Column(String(2), default=None))  # TODO: create IARC table (3 rows)

    environmental_hazard = Column(Boolean, default=None)
    other_tox = deferred(Column(Boolean, default=None))

    # reef_safe = Column(Boolean, default=None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # FIXME: add more later
        fragrances = {'parfum', 'perfume', 'fragrance', 'aroma', 'essential oil blend', 'essential oil'}
        if self.common_name.lower() in fragrances:
            self.is_fragrance = True

    # interactions1 = list of Interaction objects (adverse reactions)
    # interactions2 = list of Interaction objects (adverse reactions)
    product_ingredients = db.relationship('ProductIngredient', back_populates='ingredient')

    def __repr__(self):
        return f"<Ingredient ingredient_id={self.ingredient_id} common_name={self.common_name} active_type={self.active_type}>"


class Interaction(TimestampMixin, db.Model):
    """Create an Ingredient object for the master interactions table."""

    __tablename__ = 'interactions'

    interaction_id = Column(Integer, primary_key=True, autoincrement=True)
    first_ingredient_id = Column(Integer, db.ForeignKey('ingredients.ingredient_id'))
    second_ingredient_id = Column(Integer, db.ForeignKey('ingredients.ingredient_id'))
    reaction_description = Column(Text, nullable=False)

    ingredient1 = db.relationship('Ingredient', foreign_keys=[first_ingredient_id], backref='interactions1')
    ingredient2 = db.relationship('Ingredient', foreign_keys=[second_ingredient_id], backref='interactions2')

    def __repr__(self):
        return f"<Interaction interaction_id={self.interaction_id} first_ingredient_id={self.first_ingredient_id} second_ingredient_id={self.second_ingredient_id}>"


class ProductIngredient(TimestampMixin, db.Model):
    """Create a ProductIngredient object for the product_ingredients table."""

    __tablename__ = 'product_ingredients'

    prod_ing_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, db.ForeignKey('products.product_id'), nullable=True)
    ingredient_id = Column(Integer, db.ForeignKey('ingredients.ingredient_id'), nullable=True)    # onUpdate='cascade' ?
    abundance_order = Column(Integer)  # auto-increment, but restart at 1 for new product_id
    
    ingredient = db.relationship('Ingredient', back_populates='product_ingredients')
    product = db.relationship('Product', back_populates='product_ingredients')

    def __repr__(self):
        return f"<ProductIngredient prod_ing_id={self.prod_ing_id} product_id={self.product_id} ingredient_id={self.ingredient_id} abundance_order={self.abundance_order}>"
    

class Routine(TimestampMixin, db.Model):
    """Create a Routine object for the routines table."""

    __tablename__ = 'routines'

    routine_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, db.ForeignKey('users.user_id'), nullable=False)
    am_or_pm = Column(String(2), nullable=False)
    name = Column(String(25))
    is_active = Column(Boolean, default=True)

    user = db.relationship('User', backref='routines')
    steps = db.relationship('Step', backref='routine')

    @property
    def serialize(self):
        return {
            'routine_id': self.routine_id,
            'user_id': self.user_id,
            'name': self.name,
            'am_or_pm': self.am_or_pm,
            'is_active': self.is_active
        }
    @property
    def serialize_current_steps(self):
        return [ [ item.step_id, item.product_id ] for item in self.steps if not bool(item.retired_on) ]
    @property
    def serialize_current_steps_verbose(self):
        return [ item.serialize for item in self.steps if not bool(item.retired_on) ]
    
    def make_active(self):
        r_id = self.user.get_current_routines_id(self.am_or_pm) if self.am_or_pm else None
        old_routine = Routine.query.get(r_id) if r_id else None
            if old_routine:
                old_routine.is_active = False
        self.is_active = True
        db.commit()
        print(f'Saved routine with id {self.routine_id} as active {self.am_or_pm} routine.')

    def add_step(self, product_id):
        step_obj = Step(product_id=product_id)
        if not self.steps:
            self.steps = []
        self.steps.append(step_obj)
        return step_obj
    # def update_cardinality(self):
    #     """Save the order in which skincare steps are performed."""
    #     for step in self.steps:
    #         step.cardinal_order = something
    #     db.session.commit()

    def __repr__(self):
        return f"<Routine routine_id={self.routine_id} name={self.name} user_id={self.user_id} am_or_pm={self.am_or_pm} number of steps={len(self.steps) if self.steps else None}>"


class Step(TimestampMixin, db.Model):
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
    
    notes = Column(Text, nullable=True, default=None)

    product = db.relationship('Product', backref='steps')
    
    # dates = (list of) Frequency object(s), for usage timestamps
    # routine = Routine objects, linked to individual steps in the routine

    @property
    def serialize(self):
        return {
            'cardinal_order': self.cardinal_order,
            'dates': self.serialize_frequencies,
            'is_retired': bool(self.retired_on)
        }
    @property
    def serialize_verbose(self):
        return {
            'routine_id': self.routine_id,
            'routine_nickname': self.routine.name,
            'am_or_pm': self.routine.am_or_pm,  # can see this from Routine.serialize also
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category_id': self.product.category_id,
            'updated_on': self.updated_on,
            # 'updated_on_PT': convert_to_PST(self.updated_on)  # need to test
        }
    @property
    def serialize_dates_only(self, convert_to_PT=False):
        if convert_to_PT:
            return [ convert_to_PST(item.created_on) for item in self.dates ]
        return [ item.created_on for item in self.dates ]
    @property
    def serialize_frequencies(self):
        return [ item.serialize for item in self.dates ]

    def __init__(self, **kwargs):
        super(Step, self).__init__(**kwargs)
        if self.product.category.category_name.lower() in {'exfoliator', 'peel'}:
            concerns = set()
            if self.primary_concern_id:
                concerns.add(self.primary_concern_id)
            if self.secondary_concern_id:
                concerns.add(self.secondary_concern_id)
            if self.routine.user.skintype.skintype_name.lower() == 'sensitive' or (concerns and concerns.intersection(set(1, 3, 7, 8))):
                self.interval = 7
            else:
                self.interval = 3

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

    def un_retire(self):
        """"""
        new_step = Step(routine_id = self.routine_id)
        # FIXME: need to update cardinal_order... maybe add update_cardinality() to Routine
        db.session.add(new_step)
        db.session.commit()
    
    def __repr__(self):
        return f"<Step step_id={self.step_id} product_id={self.product_id}>"


class Frequency(TimestampMixin, db.Model):
    """Create a Frequency object to track frequency of use of each skincare step.
    Each Step object is linked to multiple Frequency objects to record:
        - timestamps for dates of use
        - notes (user feedback for themselves)
    """

    __tablename__ = 'frequencies'

    freq_id = Column(Integer, primary_key=True, autoincrement=True)
    step_id = Column(Integer, db.ForeignKey('steps.step_id'), nullable=False)
    interval = Column(Integer, default=1)
    notes = Column(Text, default=None)
    # NOTE: ALTERNATIVE WAY TO DO THIS...
        # save dates as Array of DateTimes? Or a long string that can be
        # de-string-ified to get dates out of it? Use for data visualization...
            # eg: dates = Column(Text, default=None)

    step = db.relationship('Step', backref='dates')

    @property
    def serialize(self):
        return {
            'date': self.created_on,
            'notes': self.notes
        }
    @property
    def serialize_verbose(self):
        return {
            'freq_id': self.freq_id,
            'date': self.created_on,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f"<Frequency freq_id={self.freq_id} step_name={self.step_name}>"


##### DB-RELATED FUNCTIONS BELOW #####

def connect_to_db(flask_app, db_uri="postgresql:///testdb", echo={_ECHO_LOG_ERRORS_}, to_confirm=True):
    db_name = confirm_db_name(ask_to_confirm=to_confirm)
    db_uri=f"postgresql:///{db_name}"

    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # NOTE: If set to True, Flask-SQLAlchemy will track modifications of objects and emit signals.
    # The default is None, which enables tracking but issues a warning that it will be disabled by
    # default in the future. This requires extra memory and should be disabled if not needed.
    # https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#configuration-keys

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")
    print(db_uri)


def confirm_db_name(ask_to_confirm=True):
    """Returns a valid db name based on the environment variables."""
    import os
    import sys

    from database.crud import convert_string_to_datastructure as convert

    valid_names = convert(os.environ['VALID_DB_NAMES'])
    _db_name = os.environ['CURRENT_DB_NAME']
    print(f'You are about to access the PostgreSQL database named: {_db_name}')

    # Skip this block if we are running from server.py
    if ask_to_confirm:
        change_db = input('Do you want to change to a different database? If so, type the name here. (hit enter if not)  ')

        if change_db:
            if change_db in valid_names:
                print(f'Yes! {change_db} is a valid database.')
                os.environ['CURRENT_DB_NAME'] = change_db
                _db_name = os.environ['CURRENT_DB_NAME']
            else:
                print('Sorry, this name is invalid.')
                sys.exit()

    if _db_name not in valid_names:
        print(f'Weird, it looks like {_db_name} is not a valid database. Someone should update secrets.sh!')
        print('Closing out.')
        sys.exit()
    print(f"Okay, let's proceed with {_db_name}, which is a valid database.")
    return _db_name


if __name__ == '__main__':
    print("Hello, I'm in model.py's special statement since __name__ == '__main__'!")

    from server import app

    connect_to_db(flask_app=app, echo=False)
    # db.create_all()
    print('Done running model.py!')
