import sys, os, json, csv
import crud, model, read_files
# import server  # after it is created
from random import choice, randint
from flask import Flask

os.system('dropdb project_test --if-exists')
os.system('createdb project_test')

app = Flask(__name__)

model.connect_to_db(app)
model.db.create_all()

# can use data/file_list_test2.txt to test
files_to_load = 'data/file_list_test2.txt'
added_objects_dict = read_files.main(files_to_load)

print(f'list(added_objects_dict.keys()) = {list(added_objects_dict.keys())}')
