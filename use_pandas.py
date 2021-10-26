"""Initialize the database for products table."""

print('pandas_data.py started running!')

import os
import sys

import numpy as np
import pandas as pd

from database import crud, model


def find_water(ingredients_str, delimiter):
    """Returns cardinal position of water in ingredients_str (1-indexed) if found, else returns None.

    >>> s = 'Caprylic/CapricTriglyceride, Glycine Soja (Soybean) Oil, C12-15, Alkyl Benzoate, Cyclopentasiloxane, Stearalkonium Hectorite, Undecane, Tridecane, Cetearyl Ethylhexanoate, Aqua, Caprylyl/Capryl Glucoside, Lecithin, Glycerin, Pseudoalteromonas Ferment Extract, Acetyl Tripeptide-30, Isopropyl Palmiate, Theobroma Cacao (Cocoa) Seed Butter, Dimethicone, Phospholipids, Swertia Chirata Extract, Citrulline, Tocopheryl Acetate, Pentapeptide-18, Xanthan Gum, Caprylyl Glycol, Propylene Carbonate, Urea, Potassium Sorbate, Phenoxyethanol.'
    >>> find_water(s, ',')
    10
    """
    ingredients = ingredients_str.split(delimiter)
    water = {'water', 'aqua', 'eau'}
    for i, ingred in enumerate(ingredients):
        # print(f'i = {i}, ingred is ...')
        # print(ingred) 
        if ingred.lower() in water:
            # print('found water! at position...')
            # print(i + 1)
            return i + 1, ingred
        else:
            for elem in water:
                if elem.lower() in ingred.lower():
                    # print('found water! at position...')
                    # print(i + 1)
                    return i + 1, ingred


def check_file(read_file, write_file):
    if 'xlsx' in read_file.lower():
        file = pd.ExcelFile(read_file)
        df = pd.read_excel(file)
    else:
        df = pd.read_csv(read_file)

    print(df.head())

    for i, row in df.iterrows():
        # ingred_str = df.at[i, 'ingredients']
        ingred_str = row['clean_ingreds']
        if ingred_str[0] == '[':
            ingred_str = ingred_str[1:-1]
        # print('ingred_str is...')
        # print(ingred_str)
        if isinstance(ingred_str, str):
            result = find_water(ingred_str, ',')
            # result = find_water(ingred_str, row.delimiter)
            if result:
                (val, word) = result
                df.at[i, 'water_index'] = val
                df.at[i, 'water_word'] = word
    
    if 'xlsx' in read_file.lower():
        df.to_excel(write_file, sheet_name='Updated')
    else:
        df.to_csv(write_file)
    return df


def add_water(dfs_to_modify):
    """Add 'water' to the ingredient list at the appropriate position.
    ka-1-water0.csv: no water
    ka-1-water1.csv: water is the 1st ingredient (at index = 0)
    ka-1-water2.csv: water is the 2nd ingredient
    ka-1-water3.csv: water is the 3rd ingredient
    """
    print('Starting the add_water function!')
    for i, df in enumerate(dfs_to_modify):
        ingred_col = []

        for j, row in df.iterrows():
            ingred_str = row['clean_ingreds']
            ingred_list = crud.convert_string_to_list(ingred_str)
            ingred_list[i:i] = ['water']
            ingred_col.append(str(ingred_list))

            # FIXME: the code below does not work...
            # row['clean_ingreds'] = str(ingred_list)
            # print(f'i = {i}, j = {j}')
        
        df['clean_ingreds'] = ingred_col
        df.to_csv(f'./database/ka-1-water{i + 1}.csv')
        print(f'Added "water" to {len(df)} rows at i = {i}!')
    print('Finished the add_water function!')


def merge_dfs(main_df, dfs_to_merge):
    """Merge product lists with the main file."""
    # add_water = './database/ka-1-find_water.xlsx'
    # add_water_df = pd.read_csv(add_water)
    for i, df in enumerate(dfs_to_merge):
        merged = pd.merge(main_df, df)
        merged.to_csv(f'./database/ka-1-water{i}.csv')
        print(f'Merged df{i+1}, located at ka-1-water{i}.csv')


def merge_with_main(dfs):
    main_file = './database/ka-1-clean_url.csv'
    main_df = pd.read_csv(main_file)

    merge_dfs(main_df, dfs)


if __name__ == '__main__':
    df1_no_water = pd.read_csv('./database/ka-1-water0.csv')
    df2_1st_water = pd.read_csv('./database/ka-1-water1.csv')
    df3_2nd_water = pd.read_csv('./database/ka-1-water2.csv')
    df4_3rd_water = pd.read_csv('./database/ka-1-water3.csv')

    dfs_to_merge = [df1_no_water, df2_1st_water, df3_2nd_water, df4_3rd_water]
    # merge_with_main(dfs_to_merge)

    add_water(dfs_to_merge[1:])

    # for i, df in enumerate(dfs_to_merge):
    #     filepath = f'./database/ka-1-water{i}.csv'
    #     new_df = check_file(filepath, filepath)
    #     new_df.head()

    # read_file = './database/ka-1-find_water.xlsx'
    # write_file = './database/ka-1-find_water.xlsx'
    # check_file(read_file, write_file)

    # axis = 1 --> add extra columns
    # result = pd.concat([main_df,], axis=1)  
    
    print('pandas_data.py finished running!')
