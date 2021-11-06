"""Infrequently-run functions to properly add search filters to products in the db."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pprint import pprint

from database import crud, db_info, model, read_files, tag_ingredients
from database.model import Ingredient, Product, ProductIngredient
from database.tag_ingredients import make_dict, update_sets_to_check


def tag_fragrances(ingred_obj, dict_of_types):
    for _, tag_set in dict_of_types:
        if ingred_obj.common_name.upper() in tag_set:
            ingred_obj.is_fragrance = True
        else:
            for item in tag_set:
                if item.lower() in ingred_obj.common_name.lower():
                    ingred_obj.is_fragrance = True
                    break


def tag_active_type(ingred_obj, dict_of_types):
    """Change ingred_obj's active_type field to the string key."""
    for tag, tag_set in dict_of_types:
        if ingred_obj.common_name.upper() in tag_set:
            ingred_obj.active_type = tag
            if tag.lower() == 'retinoid':
                ingred_obj.is_pregnancy_safe = False
                ingred_obj.pm_only = True
            break


def make_all_skintype_dicts():
    file_dict = tag_ingredients.update_sets_to_check()
    rec_dry = make_dict(file_dict, ['dry'])
    not_dry = make_dict(file_dict, ['not_dry'])
    rec_oily = make_dict(file_dict, ['oily'])
    not_oily = make_dict(file_dict, ['not_oily'])
    rec_sensitive = make_dict(file_dict, ['sensitive'])
    not_sensitive = make_dict(file_dict, ['not_sensitive'])


def tag_fragrance_free_products():
    """Return a list of product ids that were updated (detected a fragrance ingredient)."""
    modified_prod_ids = []
    prods = Product.query.all()
    for prod in prods:
        ingred_list = [pi.ingredient for pi in prod.product_ingredients if pi.ingredient.is_fragrance]
        if ingred_list:
            prod.fragrance_free = False
            prod.rec_sensitive = False
            modified_prod_ids.append(prod.product_id)
        # else:
        #     prod.fragrance_free = True
    model.db.session.commit()
    print(f'Detected {len(modified_prod_ids)} products that contain fragrance.')
    return modified_prod_ids


def tag_SPF_moisturizers():
    # TODO: add mists?
    subq = Product.query.filter_by(category_id=9).subquery()
    spf_prods = model.db.session.query(Product).select_entity_from(subq).filter(Product.product_name.ilike('SPF')).all()
    print(f'There are {len(spf_prods)} products with SPF in the product name.')
    modified_prod_ids = []
    bad_prod_ids = []
    types_to_check = {'spray', 'mist', 'powder', 'powdered'}
    ingreds_to_check = {'TITANIUM DIOXIDE', 'ZINC OXIDE', 'ZNO', 'TIO2'}
    for prod in spf_prods:
        name = prod.product_name.lower()
        if 'no spf' in name:
            continue
        modified_prod_ids.append(prod.product_id)
        prod.category_id=12
        if 'spray' in name or 'mist' in name or 'powder' in name:
            ingreds_set = prod.serialize_all_ingreds
            bad_ingreds = ingreds_to_check.intersection(ingreds_set)
            if bad_ingreds:
                # prod.is_carcinogenic = True  # TODO: add this column to model.py
                bad_prod_ids.append(prod.product_id)
        # model.db.session.commit()
    print(f'Detected {len(modified_prod_ids)} products that advertise SPF in the product name.')
    print(f'Of these, {len(bad_prod_ids)} products contain TiO2 or ZnO in inhalable form - which is carcinogenic!')
    return (modified_prod_ids, bad_prod_ids)


def tag_all_products():
    # prods = Product.query.all()
    ff_prods = tag_fragrance_free_products()
    print(ff_prods)
    (spf_prods, bad_spf_prods) = tag_SPF_moisturizers()
    print(spf_prods)
    print(bad_spf_prods)
    model.db.session.rollback()

if __name__ == '__main__':
    from server import app
        
    model.connect_to_db(app, echo=False)

    sunscreens = Product.query.filter(
        Product.product_name.ilike('%SPF%')
        ).all()
    
    sunscreen_summary = {}
    for prod in sunscreens:
        sunscreen_summary[prod.product_id] = prod.serialize_top_five_names
    pprint(sunscreen_summary)

    print('-'*20)
    tag_all_products()
    # main()
    print('Work in progress!')
    print('Successfully finished running tag_products.py!')
