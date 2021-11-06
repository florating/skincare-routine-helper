"""Testing how to scrape metadata"""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pprint import pprint
import time
from urllib.error import HTTPError, URLError

import cloudinary
from cloudinary.api import delete_resources_by_tag, resources_by_tag
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url
from ratelimit import limits, sleep_and_retry

from database import model

SECONDS = 30

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
def upload_file(img_url, prod_obj=None):
    # TODO: how to use public_id
    print('--- Upload a non-local file with custom public ID')
    cat_name = prod_obj.category.category_name if prod_obj else 'sunscreen/'
    tag_list = DEFAULT_TAGS

    if cat_name:
        tag_list = DEFAULT_TAGS + [cat_name.lower()]
    
    prod_id = prod_obj.product_id if prod_obj else 'eltaMDsunscreen'
    try:
        print('cat_name, tag_list, and prod_id are...')
        print(cat_name)
        print(tag_list)
        print(prod_id)
        response = upload(
            img_url,
            folder = f'skincare/{cat_name}',
            tags = tag_list,
            public_id = prod_id,
            # notification_url = '',
            resource_type = 'image'
        )

        print('-'*20)
        dump_response(response)
        
        print('-'*20)
        url, options = cloudinary_url(
            response['public_id'],
            format=response['format'],
            width=200,
            height=150,
            # gravity='faces'
            crop="fill"
        )

        print(f'Fit into 200x150 url: {url}')
        print('\n')
        print('Options are...')
        print(options)
        print('Success! The file was uploaded to Cloudinary!')

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


if __name__ == '__main__':
    from server import app
    
    start_time = time.time()
    model.connect_to_db(app)   
    print('--- %s seconds ---' % (time.time() - start_time))
    print('\n')

    test_img_url = 'https://cdn.shopify.com/s/files/1/0467/8120/2585/products/9260_Elta_D2CThumbnails_UVClear_400x400.jpg'
    print(test_img_url)
    upload_file(test_img_url)

    # print('Success!')

    print('--- %s seconds ---' % (time.time() - start_time))
