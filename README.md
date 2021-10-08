# THE SKINCARE ROUTINE HELPER

## Table Of Contents
1. [Overview](#overview)
2. [Instructions](#instructions)
3. [Next Steps](#next-steps)
4. [Completed Steps](#completed-steps)

## Overview

This is an evidence-based app to help recommend skincare products and general routines based on area of concern and ingredient safety. The app recommends products based on data analytics of user profiles, allowing users to filter for products that are reef-safe, pregnancy-safe, fragrance-free, etc.

#

## Instructions
1. Setup virtual environment:
    * `virualenv env`
    * `source env/bin/activate`
    * `pip3 install -r requirements.txt`
2. Run seed_db.py:
    * If this is your first time running the files, start with this command:
        * `createdb project_test` (Skip this step if this database already exists.)
    * `python3 seed_db.py`
3. View contents of database using PostgresQL:
    * `psql project_test`

*Further steps to be added as project development progresses!*
#
## Next Steps
#### **General:**
- [ ] request API keys
- [ ] request dataset

#### **Setup databases with sample data:**
- [ ] setup sample dataset
    - [x] 10/06: sample_products.csv: 2 dummy products with < 10 ingredients
    - [ ] generate sample_ingredients database and save somewhere
- [x] 10/06: test seeding the database for skin_concerns.json
    - [x] 10/06: seed_db.py
    - [x] 10/06: started crud.py
    - [x] 10/07: setup file to load CSV and JSON files into the database
    - [ ] setup server.py

- [ ] seed the database
    - [ ] products
    - [ ] ingredients
    - [ ] product_ingredients

#### **Display information about a product:**
- [x] setup other json files
    - [x] 10/05: about_steps.json
    - [x] 10/05: skin_concerns.json
- [ ] setup product display page

#### **Setup user login:**
- [ ] setup user login system
    - [ ] review: hashing passwords
- [ ] setup login page
- [ ] setup new user registration page

#### **Complete questionnaire for user profile:**
- [ ] complete quick questionnaire for user profile
- [ ] setup questionnaire page

#### **Setup search:**
- [ ] setup search
    - [ ] lookup search tutorials
- [ ] setup search page

#
## Completed Steps
- [x] 10/06: create data models, [using dbdiagram.io](https://dbdiagram.io/)
- [x] 10/06: setup model.py