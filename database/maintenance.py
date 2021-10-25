"""Infrequently-run functions to maintain the database or data to display for visualization purposes."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv
from datetime import datetime

import pytz

from database import crud
from database import model


def write_summary_prod_table():
    """Writes summary data for products currently in the database to '/static/files/db_summary.csv'.
    
    This also returns a list for which each element looks like the following:
        [(category_id, category_name, num_products), avg_num_ingredients]
        [(1, 'Moisturizer', 108), 31.287037037037038]
    
    NOTE: ONLY DO THIS WHENEVER THE TABLE CHANGES, AND THEN SAVE THE RESULT!
    """

    results = count_products_by_category(order_by='category_id')
    summary = []

    filepath = os.path.abspath('../static/files/db_summary.csv')
    with open(filepath, mode='w', encoding='utf-8') as db_summary_file:
        data_writer = csv.writer(db_summary_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write the row of headers first
        data_writer.writerow(['category_id', 'category_name', 'num_products', 'avg_num_ingredients', 'date_updated'])

        # Write each row of results
        for result in results:
            cat_id = result[0]
            avg_ingreds = get_avg_num_ingredients_by_category(cat_id)
            current_dt = get_current_datetime()
            data_writer.writerow([cat_id, result[1], result[2], avg_ingreds, current_dt])
            summary.append([result, avg_ingreds])
            
    return summary


def write_summary_ingredients_table():
    """SELECT c.category_name, pi.product_id, COUNT(pi.product_id) AS num_ingredients ..."""
    filepath = os.path.abspath('../static/files/db_ingred_summary.csv')
    header = ['category_id', 'category_name', 'product_id', 'num_ingredients', 'date_updated']
    with open(filepath, mode='w', encoding='utf-8') as file:
        data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(header)
        for cat_id in range(1, 15):
            results = count_ingredients_by_category(cat_id)
            for result in results:
                current_dt = get_current_datetime()
                data_writer.writerow([cat_id, result[0], result[1], result[2], current_dt])


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


def count_products_by_category(order_by='category_name'):
    """Count number of products by category_id, returning results as a list of tuples.

    Can order by "category_name" or "category_id".
        EG: [(category_id, category_name, num_products), ...]
    """
    q = 'SELECT c.category_id, c.category_name, COUNT(p.category_id) AS num_products\
        FROM products AS p\
        INNER JOIN categories AS c ON (p.category_id = c.category_id)\
        GROUP BY c.category_id, p.category_id, c.category_name\
        ORDER BY c.'
    q += order_by
    # print(f'\n\n\n q = {q}')
    cursor = model.db.session.execute(q)
    result = cursor.fetchall()
    return result


def count_ingredients_by_category(category_id):
    """Counts number of ingredients per product by category_id, returning a list of tuples."""
    q = f"SELECT c.category_name, pi.product_id, COUNT(pi.product_id) AS num_ingredients\
        FROM product_ingredients AS pi\
        JOIN products AS p ON (pi.product_id = p.product_id)\
        FULL OUTER JOIN categories AS c ON (p.category_id = c.category_id)\
        WHERE p.category_id = {category_id}\
            GROUP BY pi.product_id, p.category_id, c.category_name"
    cursor = model.db.session.execute(q)
    result = cursor.fetchall()
    return result


def get_avg_num_ingredients_by_category(cat_id=1):
    """Returns the average number of ingredients for products with this category_id."""
    # ERROR:
    # TypeError: filter() got an unexpected keyword argument 'category_id'
    prod_list = model.Product.query.filter_by(category_id=cat_id).all()

    sum_ingreds = 0
    for prod in prod_list:
        sum_ingreds += prod.get_num_ingredients()
    return sum_ingreds / len(prod_list)


if __name__ == '__main__':
    """Write a CSV file with summary info about the database."""

    from server import app

    model.connect_to_db(app)
    # write_summary_prod_table()
    write_summary_ingredients_table()
