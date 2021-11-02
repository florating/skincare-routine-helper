"""Quick info about the database, to run after seeding or adding new datasets."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pprint

from sqlalchemy import func

from database import crud, model
from database.model import (
    connect_to_db, db, Cabinet, Category, Concern, Frequency, Ingredient, Interaction, Skintype, Step, Product, ProductIngredient, Routine, User)

ALL_ORMS = [
    Cabinet, Category, Concern, Frequency, Ingredient, Interaction, Skintype, Step,
    Product, ProductIngredient, Routine, User]

VALID_DB_NAMES = {'project_test', 'project_test_2', 'testdb'}


# # # FXNS FOR INDIVIDUAL TABLES # # #
"""
NOTE: if executing raw SQL queries, check the data types returned by the fetch methods
        - fetchall() --> [(775,)] for a result with a single row
        - fetchone() --> (775,) --> <class 'sqlalchemy.engine.row.Row'>
"""
### RETURN SINGLE VALUES ###

def count_rows_orm(table_orm):
    """Given a ORM, return the # of rows in that table as an int."""
    return model.db.session.query(table_orm).count()


def count_unique_vals_sql(tablename, field):
    """Return the number of rows in this table with a unique value in a column/field."""
    QUERY = f'SELECT COUNT(DISTINCT({field})) FROM {tablename}'
    db_cursor = model.db.session.execute(QUERY)
    return db_cursor.fetchone()[0]


### RETURN MULTIPLE VALUES ###

def count_products_by_category(order_by='category_name'):
    """Count number of products by category_id or category_name, returning results as a list of tuples.
        EG: [(category_id, category_name, num_products), ...]
    """
    QUERY = """
        SELECT c.category_id, c.category_name, COUNT(p.category_id) AS num_products
        FROM products AS p
        INNER JOIN categories AS c ON (p.category_id = c.category_id)
        GROUP BY c.category_id, p.category_id, c.category_name
        ORDER BY c.
        """
    QUERY += order_by if order_by == 'category_name' else 'category_id'
    cursor = model.db.session.execute(QUERY)
    result = cursor.fetchall()
    return result


def count_ingredients_by_category(category_id):
    """Counts number of ingredients per product by category_id, returning a list of tuples."""
    QUERY = """
        SELECT c.category_name, pi.product_id, COUNT(pi.product_id) AS num_ingredients
        FROM product_ingredients AS pi
        JOIN products AS p ON (pi.product_id = p.product_id)
        FULL OUTER JOIN categories AS c ON (p.category_id = c.category_id)
        WHERE p.category_id = :category_id
        GROUP BY pi.product_id, p.category_id, c.category_name
        """
    cursor = model.db.session.execute(QUERY, {'category_id': category_id})
    result = cursor.fetchall()
    return result


def get_avg_num_ingredients_by_category(cat_id=1):
    """Returns the average number of ingredients for products with this category_id."""
    prod_list = model.Product.query.filter_by(category_id=cat_id).all()
    sum_ingreds = 0
    for prod in prod_list:
        sum_ingreds += prod.get_num_ingredients()
    return sum_ingreds / len(prod_list)


# # # FXNS FOR ALL TABLES # # #

def count_rows_all_tables_orm():
    """Return a dict of table names (str) and # of rows in the table."""    
    count_dict = {}
    for table in ALL_ORMS:
        val = count_rows_orm(table)
        count_dict[table.__name__] = val
    return count_dict


if __name__ == '__main__':
    _db_name = input('What is the name of the PostgreSQL database?  ')

    if _db_name not in VALID_DB_NAMES:
        _db_name = 'project_test_2'
    else:
        from server import app

        model.connect_to_db(app, db_uri=f"postgresql:///{_db_name}", echo=False)
        # model.db.create_all()
        results = count_rows_all_tables_orm()
        pprint.pprint(results)
