"""Infrequently-run functions to properly add search filters to products in the db."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

from pprint import pprint

from database import model, tag_ingredients
from database.model import Ingredient, Product, ProductIngredient
from database.tag_ingredients import make_dict

LIST_OF_FILES = os.path.abspath('../data/ingredient_tags/about_ingred_files.txt')


def make_all_skintype_dicts():
    """Each dict looks like: {'SKINTYPE': {'INGRED1', 'INGRED2', ...}} or {'NOT_SKINTYPE': {'INGRED1', ...}}."""
    file_dict = tag_ingredients.update_sets_to_check()
    return make_dict(file_dict, ['dry', 'not_dry', 'oily', 'not_oily', 'sensitive', 'not_sensitive'])


def tag_all_skintype_recs():
    skintype_dicts = make_all_skintype_dicts()
    skintypes = {'DRY', 'COMBINATION', 'OILY', 'SENSITIVE', 'NORMAL'}
    prod_objs = model.Product.query.all()
    for prod in prod_objs:
        tag_skintype_recs(prod, skintypes, skintype_dicts)
    model.db.session.commit()


def tag_skintype_recs(prod_obj, skintypes, skintype_dicts):
    """For a single product object, check for skintype recommendations."""
    prod_ingreds_t5 = prod_obj.serialize_top_five_names  # uppercase
    prod_ingreds_t10 = prod_obj.serialize_top_five_names  # uppercase
    prod_ingreds = prod_obj.serialize_all_ingreds  # uppercase

    for sk in skintypes:
        ingred_set = skintype_dicts.get(f'NOT_{sk}')
        if not ingred_set:
            continue
        if prod_ingreds_t5.intersection(ingred_set) or (
            prod_ingreds_t10.intersection(ingred_set) and len(prod_ingreds_t10.intersection(ingred_set)) > 3):
            if sk == 'DRY':
                prod_obj.rec_dry = True
            elif sk == 'COMBINATION':
                prod_obj.rec_combination = True
            elif sk == 'OILY':
                prod_obj.rec_oily = True
            elif sk == 'SENSITIVE':
                prod_obj.rec_sensitive = True
            elif sk == 'NORMAL':
                prod_obj.rec_normal = True
        else:
        # overwrite True values, since it's more serious to come across a bad ingredient
            ingred_set = skintype_dicts.get(f'NOT_{sk}')
            if not ingred_set:
                continue
            if prod_ingreds_t10.intersection(ingred_set):
                if sk == 'DRY':
                    prod_obj.rec_dry = False
                elif sk == 'COMBINATION':
                    prod_obj.rec_combination = False
                elif sk == 'OILY':
                    prod_obj.rec_oily = False
                elif sk == 'NORMAL':
                    prod_obj.rec_normal = False
            elif prod_ingreds.intersection(ingred_set):
                if sk == 'SENSITIVE':
                    prod_obj.rec_sensitive = False
                if len(prod_ingreds.intersection(ingred_set)) > 5:
                    if sk == 'DRY':
                        prod_obj.rec_dry = False


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


def tag_SPF_moisturizers(cat_id=7):
    results = model.db.session.query(Product)
    if isinstance(cat_id, list):
        results = results.filter(Product.category_id.in_(cat_id))
    else:
        results = results.filter(Product.category_id == cat_id)
    results = results.filter(Product.product_name.ilike('%SPF%'))
    
    spf_prod_objs = results.all()

    print(f'There are {len(spf_prod_objs)} products with SPF in the product name.')
    modified_prod_ids = []
    bad_prod_ids = []
    # types_to_check = {'spray', 'mist', 'powder', 'powdered'}
    ingreds_to_check = {'TITANIUM DIOXIDE', 'ZINC OXIDE', 'ZNO', 'TIO2'}
    for prod_obj in spf_prod_objs:
        name = prod_obj.product_name.lower()
        if 'no spf' in name:
            continue
        modified_prod_ids.append(prod_obj.product_id)
        prod_obj.category_id=12
        if 'spray' in name or 'mist' in name or 'powder' in name or cat_id == 7:
            ingreds_set = prod_obj.serialize_all_ingreds  # uppercase
            bad_ingreds = ingreds_to_check.intersection(ingreds_set)
            if bad_ingreds:
                # prod_obj.is_carcinogenic = True  # TODO: add this column to model.py
                bad_prod_ids.append(prod_obj.product_id)
        model.db.session.commit()
    print(f'Detected {len(modified_prod_ids)} products that advertise SPF in the product name.')
    print(f'Of these, {len(bad_prod_ids)} products contain TiO2 or ZnO in inhalable form - which is carcinogenic!')
    return (modified_prod_ids, bad_prod_ids)


def tag_all_products():
    # prods = Product.query.all()
    ff_prods = tag_fragrance_free_products()
    print(ff_prods)
    (spf_prods, bad_spf_prods) = tag_SPF_moisturizers([5, 6, 7, 9, 10])
    print(spf_prods)
    print(bad_spf_prods)
    model.db.session.commit()
    # model.db.session.rollback()


def main():
    # file_dict = update_sets_to_check(LIST_OF_FILES)
    # pprint(file_dict)

    tag_all_products()
    tag_all_skintype_recs()
    # db.session.commit()


if __name__ == '__main__':
    from server import app
        
    model.connect_to_db(app, echo=False)

    print('-'*20)
    main()

    print('Work in progress!')
    print('Successfully finished running tag_products.py!')
