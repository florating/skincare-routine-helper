# THE SKINCARE ROUTINE HELPER

## Table Of Contents
1. [Overview](#overview)
2. [Instructions](#instructions)
3. [Next Steps](#next-steps)
4. [Task List](#task-list)


## Overview
This is an evidence-based app to help recommend skincare products and general skincare routines based on area of concern and ingredient safety. The app recommends products based on data analytics of user profiles, allowing users to filter for products that are reef-safe, pregnancy-safe, fragrance-free, etc. Users can start with a beginner-friendly skincare routine, and they can eventually level up to more advanced routines consisting of multiple steps and usage frequencies (per product or step) depending on active ingredients.


## Instructions
1. Setup virtual environment:
    * `virualenv env`
    * `source env/bin/activate`
    * `pip3 install -r requirements.txt`
2. Run seed_db.py:
    * `python3 seed_db.py`
3. View contents of database using PostgreSQL:
    * `psql project_test`

*Further steps to be added as project development progresses!*

*[Click here](#the-skincare-routine-helper) to go back to the top.*


## Next Steps
- [ ] request API keys
- [ ] request dataset
- [x] 10/08: setup the server
- [ ] setup the homepage


## Task List
#### **General:**
- [ ] request API keys
- [ ] request dataset
- [x] 10/08: setup the server
- [ ] setup the homepage

#### **Data model:**
- [x] 10/06: create data models, [using dbdiagram.io](https://dbdiagram.io/)
- [x] 10/06: setup model.py
- [ ] add liked/disliked products
    - [ ] sanitize comment section

#### **Setup database with actual data:**
- [ ] setup Kaggle dataset with clean ingredients (CSV file)
- [ ] setup other dataset
- [ ] look for datasets with sunscreen info

#### **Display information about a product:**
- [x] setup other json files
    - [x] 10/05: about_steps.json
    - [x] 10/05: skin_concerns.json
- [ ] setup product display page

#### **Setup user login:**
- [ ] setup user login system
    - [x] review: hashing passwords
    - [x] 10/09: setup basic login system
    - [ ] setup login system using flask-login
- [x] 10/08: setup login page
- [x] 10/08: setup new user registration page
- [x] confirm that this connects to the database

#### **Complete questionnaire for user profile:**
- [ ] complete quick questionnaire for user profile
- [ ] setup questionnaire page

#### **Setup search:**
- [ ] setup search
    - [x] 10/09: lookup search tutorials
    - [x] 10/09: setup basic search using SQL queries
    - [x] 10/09: setup search using crud functions
    - [ ] test search functions
- [ ] setup search page

#### **Testing:**
- [x] 10/09: setup test_crud.py
- [ ] setup test_model.py
- [ ] setup test_server.py

*[Click here](#the-skincare-routine-helper) to go back to the top.*


## Completed Steps

#### **Setup database with sample data:**
- [x] 10/07: setup sample dataset
    - [x] 10/06: sample_products.csv: 2 dummy products with < 10 ingredients
    - [x] 10/07: populated tables with no dependencies using sample data
        - specifically: concerns, categories, skintypes, skincare_steps
    - [x] 10/07: generate sample_ingredients database
    - [ ] save somewhere
- [x] 10/06: test seeding the database for skin_concerns.json
    - [x] 10/06: seed_db.py
    - [x] 10/06: started crud.py
    - [x] 10/07: setup file to load CSV and JSON files into the database
- [x] 10/07: seed the database
    - [x] 10/07: products
    - [x] 10/07: ingredients
    - [x] 10/07: product_ingredients

*[Click here](#the-skincare-routine-helper) to go back to the top.*