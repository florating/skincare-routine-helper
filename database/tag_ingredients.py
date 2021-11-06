"""Infrequently-run functions to properly add search filters to ingredients in the db."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv
from pprint import pprint

from database import crud, db_info, model, read_files


LIST_OF_FILES = os.path.abspath('../data/ingredient_tags/about_ingred_files.txt')

VALID_DB_NAMES = {'project_test', 'project_test_2', 'testdb'}


def update_sets_to_check(file_list=LIST_OF_FILES):
    """Returns a dictionary of tags and filepaths (that contain lists of ingredient names for that tag)."""
    file_dict = {}
    with open(file_list, mode='r', encoding='utf-8-sig') as f:
        print("success!")
        data = f.readlines()
        for line in data:
            tag, filepath = line.split()
            # TODO: setup generic function to read files
            file_dict[tag.strip(',').upper()] = filepath
    return file_dict


def tag_hydration(ingred_obj, ingred_type_set):
    """If the ingredient is a member of the set of this ingred_type (eg: emollients), change its respecive is_INGRED_TYPE attribute to True."""
    for tag, filepath in file_dict.items():
        # read_files
        pass
    if ingred_obj.common_name in ingred_type_set:
        pass


def tag_fragrances(ingred_obj, dict_of_types):
    for tag, tag_set in dict_of_types:
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


def tag_hydration_type(ingred_obj, dict_of_types):
    """Change ingred_obj's active_type field to the string key."""
    for tag, tag_set in dict_of_types:
        if ingred_obj.common_name.lower() in tag_set:
            ingred_obj.hydration_type = tag
            break


def tag_special_type(ingred_obj, dict_of_types):
    """Special types include: comedogenic (more may be added)"""
    for tag, tag_set in dict_of_types:
        if ingred_obj.common_name.upper() in tag_set:
            ingred_obj.special_type = tag
            break


def make_dict(file_dict, tag_list):
    """Return a dict of string tags paired to sets of ingredient names."""
    tag_dict = {}
    for tag in tag_list:
        if tag.upper() in file_dict:
            filepath = file_dict['tag.upper()']
            with open(filepath, mode='r') as file:
                ingred_names = { line.upper() for line in file.readlines() }
                tag_dict[tag.upper()] = ingred_names
    return tag_dict


def tag_all_ingredients(file_dict):
    # Make ingredient tags (dicts of nested sets)
    exfoliant_dict = make_dict(file_dict, ['AHA', 'BHA', 'PHA'])
    other_actives_dict = make_dict(file_dict, ['retinoid', 'sunscreen', 'vitamin C'])
    all_actives_dict = {**exfoliant_dict, **other_actives_dict}
    hydration_dict = make_dict(file_dict, ['emollient', 'humectant', 'occlusive'])
    special_types_dict = make_dict(file_dict, ['comedogenic'])
    formaldehyde_dict = make_dict(file_dict, ['formaldehyde'])

    # FIXME: convert from CSV --> txt file
    sunscreen_dict = make_dict(file_dict, ['sunscreen'])
    
    silicone_dict = make_dict(file_dict, ['silicone'])
    sulfate_dict = make_dict(file_dict, ['sulfate'])
    phthalate_dict = make_dict(file_dict, ['phthalate'])
    paraben_dict = make_dict(file_dict, ['paraben'])

    # Query for all ingredients in the db
    ingred_objs = model.Ingredient.query.limit(5).all()
    for ingred in ingred_objs:
        # This also checks for pm_only and is_pregnancy_safe fields
        tag_active_type(ingred, all_actives_dict)

        tag_hydration_type(ingred, hydration_dict)
        tag_special_type(ingred, special_types_dict)
        tag_fragrances(ingred, make_dict(file_dict, ['fragrance']))


def main():
    file_dict = update_sets_to_check(LIST_OF_FILES)
    pprint(file_dict)

if __name__ == '__main__':
    from server import app

    model.connect_to_db(app, echo=False)

    print('the_file_dict:')
    the_file_dict = update_sets_to_check(LIST_OF_FILES)
    pprint(the_file_dict)

    print('exfoliant_dict:')
    exfoliant_dict = make_dict(the_file_dict, ['AHA', 'BHA', 'PHA'])
    pprint(exfoliant_dict)

    # main()
    print('Work in progress!')
    print('Successfully finished running tag_ingredients.py!')
