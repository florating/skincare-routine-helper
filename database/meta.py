"""Testing how to scrape metadata"""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv
from pprint import pprint
from urllib.request import urlopen

from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry

from database import crud, db_info, model

VALID_DB_NAMES = {'project_test', 'project_test_2', 'testdb'}

ONE_MINUTE = 60

test_url = 'https://www.lookfantastic.com/cerave-facial-moisturising-lotion-no-spf-52ml/11798688.html'

# get_data(test_url)

"""
The result from the above test_url was:
    CeraVe Facial Moisturising Lotion No SPF 52ml
    https://static.thcdn.com/images/small/original/productimg/960/960/11798688-1194696099173549.jpg
SOURCES:
    https://stackoverflow.com/questions/36768068/get-meta-tag-content-property-with-beautifulsoup-and-python
    https://stackoverflow.com/questions/66533085/get-meta-tag-content-by-name-beautiful-soup-and-python
"""

@sleep_and_retry
@limits(calls=3, period=ONE_MINUTE)
def get_data(url):
    print("Let's get some data!")
    with urlopen(url) as webpage:
        soup = BeautifulSoup(webpage, features='html.parser')

        title = soup.find('meta', attrs={'property': 'og:title'})
        title_content = title['content'] if title else 'No meta title given'
        print(title_content)

        image = soup.find('meta', {'property': 'og:image'})
        image_content = image['content'] if image else 'No meta url given'
        print(image_content)

        return (title, title_content, image, image_content)


def get_product_ids(cat_name, set_limit=False):
    """Return a list of tuples for products from a specific product category (eg: Moisturizer).
    Tuple format: (category_id, category_name, product_id, product_url)
    """
    cat_id = crud.get_obj_by_param('Category', **{'category_name': cat_name}).category_id
    prod_list = model.Product.query.filter_by(category_id=cat_id)
    if set_limit:
        prod_list = prod_list.limit(5)
    return [(prod.category_id, cat_name, prod.product_id, prod.product_url) for prod in prod_list.all()]


def write_metadata_to_csv(tup_list):
    """Tuple format: (category_id, category_name, product_id, product_url)"""
    summary = []

    filepath = os.path.abspath('../static/files/prod_metadata.csv')
    with open(filepath, mode='w', encoding='utf-8') as metadata:
        data_writer = csv.writer(metadata, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write the row of headers first
        data_writer.writerow(['category_id', 'category_name', 'product_id', 'product_url', 'meta_title', 'meta_img', 'date_updated'])

        # Write each row of results
        for result in tup_list:
            (cat_id, cat_name, prod_id, prod_url) = result
            current_dt = model.get_current_datetime()

            (title, title_content, image, image_content) = get_data(prod_url)

            data_writer.writerow([
                cat_id, cat_name, prod_id, prod_url,
                title, title_content, image, image_content, current_dt])
            summary.append([result, title, title_content, image, image_content])
            
    return summary


if __name__ == '__main__':
    from server import app

    _db_name = input('What is the name of the PostgreSQL database?  ')

    if _db_name in VALID_DB_NAMES:
        db_uri = f'postgresql:///{_db_name}'
        model.connect_to_db(app, db_uri, echo=False)

        moist_prods = get_product_ids('Moisturizer', set_limit=True)
        clean_prods = get_product_ids('Cleanser', set_limit=True)
        # pprint(moist_prods)
        # pprint(clean_prods)

        # iterate through the list of prod_ids to get_data
        # write the returned (title, image) values into a csv
        results = []
        print('Starting with moist_prods...')
        results.extend(write_metadata_to_csv(moist_prods))
        print('Starting with clean_prods...')
        results.extend(write_metadata_to_csv(clean_prods))
        print('Success!')
        print(results)
    else:
        print('That is not a valid database name. Sorry.')
