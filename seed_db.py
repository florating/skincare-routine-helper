import sys, os, json, csv
import crud, model, read_files
# import server  # after it is created
from random import choice, randint
from flask import Flask

os.system('dropdb project_test')
os.system('createdb project_test')

app = Flask(__name__)

model.connect_to_db(app)
model.db.create_all()

# concerns_in_db = []
# obj_in_db = []

files_to_load = 'data/file_list.txt'
added_objects_dict = read_files.main(files_to_load)

print(f'added_objects_dict.keys() = {added_objects_dict.keys()}')

# with open('data/skin_concerns.json') as f:
#     data = json.loads(f.read())
#     for el in data:
#         obj = crud.create_table_obj('Concern', **el)
#         obj_in_db.append(obj)

    # for el in data:
    #     print(f'el["concern_name"]={el["concern_name"]}')

    #     con = crud.create_concern(name=el['concern_name'], desc=el['description'])
    #     concerns_in_db.append(con)
