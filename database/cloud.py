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

import cloudinary
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from ratelimit import limits, sleep_and_retry

from database import meta, model, model_helpers

SECONDS = 30

_FILEPATH = os.path.abspath('../static/files/prod_image_urls.csv')

DEFAULT_TAGS = ['skincare', 'product']

# NOTE: https://github.com/cloudinary/pycloudinary

# config from here: https://github.com/cloudinary/pycloudinary/blob/master/samples/basic/basic.py
os.chdir(os.path.join(os.path.dirname(sys.argv[0]), '.'))
if os.path.exists('settings.py'):
    exec(open('settings.py').read())


def dump_response(response):
    print('Upload response:')
    for key in sorted(response.keys()):
        print(f' {key}: {response[key]} ')


def example_upload():
    test_img_url = 'https://cdn.shopify.com/s/files/1/0467/8120/2585/products/9260_Elta_D2CThumbnails_UVClear_400x400.jpg'

    # http://res.cloudinary.com/demo/image/upload/sample_remote.jpg
    upload(test_img_url, public_id = 'eltaMDsunscreen')
    cloudinary.utils.cloudinary_url('eltaMDsunscreen.jpg')


@sleep_and_retry
@limits(calls=1, period=SECONDS)
def upload_file(img_url, cat_name, prod_id, prod_obj=None):
    # print('--- Upload a non-local file with custom public ID')
    tag_list = DEFAULT_TAGS + [cat_name.lower()]
    if not prod_obj:
        prod_obj = model.Product.get(prod_id) if prod_id else None

    try:
        # print('cat_name, tag_list, and prod_id are...')
        # print(cat_name)
        # print(tag_list)
        # print(prod_id)
        response = upload(
            img_url,
            folder = f'skincare/',
            tags = tag_list,
            public_id = prod_id,
            # notification_url = '',
            resource_type = 'image'
        )

        print('-'*20)
        res = dump_response(response)
        res_public_id = response['public_id']
        res_url = response['url']
        res_secure_url = response['secure_url']
        res_width = response['width']
        res_height = response['height']
        res_tags = response['tags']
        
        prod_obj.cloud_img_url = res_secure_url
        model.db.session.commit()

        print('-'*20)
        thumb_url, options = cloudinary_url(
            response['public_id'],
            format=response['format'],
            width=100,
            gravity='auto',
            crop="fill"
        )

        # CloudinaryImage("lady.jpg").image(transformation=[
        #     {'gravity': "face", 'height': 100, 'width': 100, 'crop': "thumb"},
        #     {'radius': "max"},
        #     {'overlay': "cloudinary_icon_white"},
        #     {'flags': "relative", 'width': "0.5", 'crop': "scale"},
        #     {'opacity': 60},
        #     {'effect': "brightness:100"},
        #     {'flags': "layer_apply"},
        #     {'dpr': "2.0"}
        #     ])

        # print(f'Fit into 200x200 url: {url}')
        print('\n')
        print('Options are...')
        print(options)
        print('Success! The file was uploaded to Cloudinary!')
        return [res_public_id, res_url, res_secure_url, res_tags, thumb_url]

    except HTTPError as e:
        print(f'HTTPError code: {e.code}')
        print(f'For url: {url}')
        return (None, None, 'HTTPError', e.code)

    except URLError as e:
        print(f'URLError code: {e.reason}')
        print(f'For url: {url}')
        return (None, None, 'URLError', e.reason)


def cleanup(tag=DEFAULT_TAGS):
    response = resources_by_tag(tag)
    resources = response.get('resources', [])
    if not resources:
        print("No images found")
        return
    print("Deleting {0:d} images...".format(len(resources)))
    delete_resources_by_tag(tag)
    print("Done!")


def write_urls_to_csv(tup_list_to_upload, prods_to_skip=None):
    """Tuple format: (category_id, category_name, product_id, product_url, title_content, image_url)"""
    summary = []

    with open(_FILEPATH, mode='a', encoding='utf-8') as metadata:
        data_writer = csv.writer(metadata, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)

        # Write the row of headers first (if not yet done)
        # data_writer.writerow(['date_updated', 'category_id', 'category_name', 'product_id', 'product_url',
        #     'title_content',
        #     'img_content', 'public_id', 'cloud_url', 'cloud_url_secure', 'image_tags', 'cloud_url_thumb'])

        # Write each row of results
        for result in tup_list_to_upload:
            if not result:
                continue
            
            print('The result:')
            print(result)
            (cat_id, cat_name, prod_id, prod_url, prod_title, img_url) = result
            current_dt = model_helpers.get_current_datetime()

            if not prod_id or prod_id in prods_to_skip or img_url in {'404', 'No meta url given'}:
                # print(f'{prod_id} is in prods_to_skip! continue...')
                continue
            
            prod_obj = model.Product.query.get(prod_id)
            upload_result = []
            # FIXME: change after testing
            upload_result = upload_file(img_url=img_url, cat_name=cat_name, prod_id=prod_id, prod_obj=prod_obj)
            (public_id, cloud_url, cloud_url_secure, image_tags, thumb_url) = upload_result

            row = [current_dt, cat_id, cat_name, prod_id, prod_url, prod_title, img_url] + upload_result

            data_writer.writerow(row)
            summary.append(row[1:])
    return summary


def get_product_ids_to_upload(category, filepath=os.path.abspath('../static/files/prod_metadata.csv')):
    """Get list of product_ids from the scraped metadata of a specific category.
    EXAMPLE: (1,'Cleanser', 508, https://static.thcdn.com/images/small/original//productimg/960/960/11798697-7344774893144504.jpg)"""
    rows_to_check = []

    with open(filepath, mode='r', encoding='utf-8') as metadata:
        csvreader = csv.DictReader(metadata)

        for row in csvreader:
            # pprint(row)
            if row['category_name'] == category:
                rows_to_check.append((
                    int(row['category_id']),
                    row['category_name'],
                    int(row['product_id']),
                    row['product_url'],
                    row['title_content'],
                    row['img_content']))
    
    print(f'\n\nSuccessfully found {len(rows_to_check)} rows that already have data in the img_content field in category={category}.\n\n')
    return rows_to_check


if __name__ == '__main__':
    from server import app
    
    start_time = time.time()
    model.connect_to_db(app, echo=False)   
    print('--- %s seconds ---' % (time.time() - start_time))
    print('\n')

    _category = input('Which product category do you want to query? (eg: Cleanser)  ')

    # Skip products that have already been uploaded to Cloudinary
    prods_in_cloud = meta.get_product_ids_and_checked_metadata(upload=True, filepath=_FILEPATH)
    prods_to_skip = meta.get_checked_prod_ids(prods_in_cloud)

    # Get the list of products to upload to Cloudinary
    prods_to_upload = get_product_ids_to_upload(_category)
    _limit = input(f'Do you want to limit this query? (Enter a number <{len(prods_to_upload)} else leave blank)  ')
    if _limit:
        prods_to_upload = prods_to_upload[:int(_limit)]
    print(f'Okay. Uploading {len(prods_to_upload)} {_category} products to Cloudinary.')
    # example: prods_to_upload[0]
        # ('1', 'Cleanser', 508, 'https://www.lookfantastic.com/cerave-foaming-facial-cleanser-473ml/11798697.html', 'CeraVe Foaming Facial Cleanser 473ml', 'https://static.thcdn.com/images/small/original//productimg/960/960/11798697-7344774893144504.jpg')
    print('-' * 20)
    print('\n# of prods_to_skip')
    print(len(prods_to_skip))
    if prods_to_skip:
        print(prods_to_skip)  # eg: {508, 509} for product_id values as ints

    print('\n# of prods_in_cloud')
    print(len(prods_in_cloud))
    if prods_in_cloud:
        print('prods_in_cloud[0]')
        print(prods_in_cloud[0])  # eg: ('508', 'https://static.thcdn.com/images/small/original//productimg/960/960/11798697-7344774893144504.jpg')

    print('\n# of prods_to_upload')
    print(len(prods_to_upload))
    if prods_to_upload:
        print('prods_to_upload[0]')
        print(prods_to_upload[0])  # eg: (1, 'Cleanser', 508, 'https://www.lookfantastic.com/cerave-foaming-facial-cleanser-473ml/11798697.html', 'CeraVe Foaming Facial Cleanser 473ml', 'https://static.thcdn.com/images/small/original//productimg/960/960/11798697-7344774893144504.jpg')

    # test_img_url = 'https://cdn.shopify.com/s/files/1/0467/8120/2585/products/9260_Elta_D2CThumbnails_UVClear_400x400.jpg'
    # print(test_img_url)
    # upload_file(test_img_url)

    upload_results = []
    res = write_urls_to_csv(prods_to_upload, prods_to_skip=prods_to_skip)
    upload_results.extend(res)
    print(upload_results)
    
    print(f'\n# products uploaded: {len(upload_results)}')

    # Confirm whether the db is still connected
    print('model.db')
    print(model.db)

    print('Success!')
    print('--- %s seconds ---' % (time.time() - start_time))
