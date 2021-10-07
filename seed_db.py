import sys, os, json
import crud, model
# import server  # after it is created
from random import choice, randint
from flask import Flask

os.system('dropdb project_test')
os.system('createdb project_test')

app = Flask(__name__)

model.connect_to_db(app)
model.db.create_all()

concerns_in_db = []

with open('data/skin_concerns.json') as f:
    data = json.loads(f.read())
    for el in data:
        print(f'el["concern_name"]={el["concern_name"]}')
        obj = crud.create_concern(**el)
        concerns_in_db.append(obj)