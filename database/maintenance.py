"""Infrequently-run functions to maintain the database or data to display for visualization purposes."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv

from database import crud, db_info, model

VALID_DB_NAMES = {'project_test', 'project_test_2', 'testdb'}


def write_summary_prod_table():
    """Writes summary data for products currently in the database to '/static/files/db_summary.csv'.
    NOTE: ONLY DO THIS WHENEVER THE TABLE CHANGES, AND THEN SAVE THE RESULT!
    This also returns a list for which each element looks like the following:
        [(category_id, category_name, num_products), avg_num_ingredients]
        [(1, 'Moisturizer', 108), 31.287037037037038]
    """

    results = db_info.count_products_by_category(order_by='category_id')
    summary = []

    filepath = os.path.abspath('../static/files/db_summary.csv')
    with open(filepath, mode='w', encoding='utf-8') as db_summary_file:
        data_writer = csv.writer(db_summary_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write the row of headers first
        data_writer.writerow(['category_id', 'category_name', 'num_products', 'avg_num_ingredients', 'date_updated'])

        # Write each row of results
        for result in results:
            cat_id = result[0]
            avg_ingreds = db_info.get_avg_num_ingredients_by_category(cat_id)
            current_dt = model.get_current_datetime()  # FIXME: change to isoformat?
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
            results = db_info.count_ingredients_by_category(cat_id)
            for result in results:
                current_dt = model.get_current_datetime()
                data_writer.writerow([cat_id, result[0], result[1], result[2], current_dt])


if __name__ == '__main__':
    """Write a CSV file with summary info about the database."""

    from server import app

    _db_name = input('What is the name of the PostgreSQL database?  ')

    if _db_name in VALID_DB_NAMES:
        db_uri = f'postgresql:///{_db_name}'
        model.connect_to_db(app, db_uri, echo=False)
        write_summary_prod_table()
        write_summary_ingredients_table()
        print('Success!')
    else:
        print('That is not a valid database name. Sorry.')
