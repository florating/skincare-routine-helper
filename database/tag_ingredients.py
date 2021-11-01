"""Infrequently-run functions to properly add search filters to ingredients in the db."""

# # # This code is for connecting nested directories/files/making variables accessable # # #
import os
import sys

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_PATH)
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import csv

from database import crud, model, read_files

LIST_OF_FILES = os.path.abspath('./ingredient_tags/about_files.txt')

ATTR_DICT = {
    'emollients': model.Ingredient.is_emollient,
    'fragrances': model.Ingredient.is_fragrance,
    'humectants': model.Ingredient.is_humectant,
    'occlusives': model.Ingredient.is_occlusive,
}

TAG_DICT = {}


def update_sets_to_check(file_list=LIST_OF_FILES):
    """Returns a dictionary of tags and filepaths (that contain lists of ingredient names for that tag)."""
    file_dict = {}
    with open(file_list, mode='r', encoding='utf-8-sig') as f:
        print("success!")
        data = f.readlines()
        for line in data:
            tag, filepath, other = line.split()
            # TODO: setup generic function to read files
            file_dict[tag] = filepath
    return file_dict


def tag_emollients(ingred_obj, ingred_type_set):
    """If the ingredient is a member of the set of this ingred_type (eg: emollients), change its respecive is_INGRED_TYPE attribute to True."""
    for tag, filepath in file_dict.items():
        # read_files
        pass
    if ingred_obj.common_name in ingred_type_set:
        pass


def tag_fragrances(ingred_obj, ingred_type_set):
    if ingred_obj.common_name.lower() in ingred_type_set:
        ingred_obj.is_fragrance = True
    else:
        for item in ingred_type_set:
            if item.lower() in ingred_obj.common_name.lower():
                ingred_obj.is_fragrance = True
                break


def tag_all_types(file_dict):
    pass


def tag_all_hazards(file_dict):
    pass


def main():
    file_dict = update_sets_to_check(LIST_OF_FILES)
    all_ingreds = model.Ingredient.query.all()
    for ingred in all_ingreds:
        tag_emollients(ingred, )
    db.session.commit()


if __name__ == '__main__':
    # main()
    print('TODO: Work in progress!')
