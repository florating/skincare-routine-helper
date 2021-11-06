"""Testing how to scrape metadata"""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv
from pprint import pprint
import time
from urllib.error import HTTPError, URLError
from urllib.request import urlopen

from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry

from database import crud, db_info, model

VALID_DB_NAMES = {'project_test', 'project_test_2', 'testdb'}

SECONDS = 30

_FILEPATH = os.path.abspath('../static/files/prod_metadata.csv')

"""
NOTE: check current categories and # of products using this query:
    SELECT c.category_id, c.category_name, COUNT(p.product_name) AS num_products FROM categories AS c FULL OUTER JOIN products AS p ON (c.category_id= p.category_id) GROUP BY c.category_id ORDER BY c.category_id;
"""

@sleep_and_retry
@limits(calls=1, period=SECONDS)
def get_data(url):
    """Scrape image url from metadata using Beautiful Soup with rate limits."""
    print("Let's get some data!")
    try:
        with urlopen(url) as webpage:
            soup = BeautifulSoup(webpage, features='html.parser')

            title = soup.find('meta', attrs={'property': 'og:title'})
            title_content = title['content'] if title else 'No meta title given'
            print(title_content)

            image = soup.find('meta', {'property': 'og:image'})
            image_content = image['content'] if image else 'No meta url given'
            print(image_content)

            return (title, title_content, image, image_content)
    except HTTPError as e:
        print(f'HTTPError code: {e.code}')
        print(f'For url: {url}')
        return (None, None, 'HTTPError', e.code)
    except URLError as e:
        print(f'URLError code: {e.reason}')
        print(f'For url: {url}')
        return (None, None, 'URLError', e.reason)


def get_product_ids(cat_name, set_limit=10):
    """Return a list of tuples for products from a specific product category (eg: Moisturizer).
    Tuple format: (category_id, category_name, product_id, product_url)
    """
    cat_id = crud.get_obj_by_param('Category', **{'category_name': cat_name}).category_id
    prod_list = model.Product.query.filter_by(category_id=cat_id)
    if set_limit:
        prod_list = prod_list.limit(set_limit)
    return [(prod.category_id, cat_name, prod.product_id, prod.product_url) for prod in prod_list.all()]


def get_product_ids_and_checked_metadata(filepath=_FILEPATH):
    """Return a list of tuples for product ids and image URLs that have already been checked."""
    checked_rows = []
    with open(filepath, mode='r', encoding='utf-8') as written_metadata:
        csvreader = csv.DictReader(written_metadata)
        
        # NOTE: row = {'category_id': 9, 'category_name': 'Moisturizer', ...}
        # HEADERS: date_updated, category_id, category_name, product_id, product_url, meta_title, title_content, meta_img, img_content

        for row in csvreader:
            # pprint(row)
            if row['img_content']:
                checked_rows.append((row['product_id'], row['img_content']))

    print(f'\n\nSuccessfully found {len(checked_rows)} rows that already have data in the img_content field.\n\n')
    return checked_rows


def get_checked_prod_ids(tuple_list):
    """Returns a set of product ids for which a check on metadata has already been made."""
    if not tuple_list:
        tuple_list = get_product_ids_and_checked_metadata()
    return {int(tup[0]) for tup in tuple_list if tup[1]}


def write_metadata_to_csv(tup_list, prods_to_skip=None):
    """Tuple format: (category_id, category_name, product_id, product_url)"""
    summary = []

    with open(_FILEPATH, mode='a', encoding='utf-8') as metadata:
        data_writer = csv.writer(metadata, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # Write the row of headers first (if not yet done)
        # data_writer.writerow(['category_id', 'category_name', 'product_id', 'product_url', 'meta_title', 'title_content', 'meta_img', 'img_content', 'date_updated'])

        # Write each row of results
        for result in tup_list:
            if not result:
                continue
            (cat_id, cat_name, prod_id, prod_url) = result
            current_dt = model.get_current_datetime()
            
            if not prod_id or prod_id in prods_to_skip:
                # print(f'{prod_id} is in prods_to_skip! continue...')
                continue

            # print(f'{prod_id} is not in prods_to_skip! append to summary...')
            (title, title_content, image, image_content) = get_data(prod_url)
            data_writer.writerow([
                current_dt, cat_id, cat_name, prod_id, prod_url,
                title, title_content, image, image_content])
            summary.append([result, title, title_content, image, image_content])

    print('Done with write_metadata_to_csv!')
    return summary


if __name__ == '__main__':
    from server import app

    start_time = time.time()
    model.connect_to_db(app, echo=False)

    print('--- %s seconds ---' % (time.time() - start_time))
    print('\n')

    _category = input('Which product category do you want to query? (eg: Cleanser)  ')
    _limit = input('Do you want to limit this query? (Enter a number <100 else leave blank)  ')
    
    prods = get_product_ids(_category, set_limit=_limit)
    already_checked = get_product_ids_and_checked_metadata()
    prods_to_skip_set = get_checked_prod_ids(already_checked)
    pprint('prods_to_skip_set:')
    print(prods_to_skip_set)
    print('--- %s seconds ---' % (time.time() - start_time))
    print('\n')
    # iterate through the list of prod_ids to get_data
    # write the returned (title, image) values into a csv
    results = []
    results.extend(write_metadata_to_csv(prods, prods_to_skip_set))
    print('--- %s seconds ---' % (time.time() - start_time))
    print('\n')
    print('Success!')
    # print(results)
