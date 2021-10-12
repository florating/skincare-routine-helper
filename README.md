# THE SKINCARE ROUTINE HELPER

## Table Of Contents
1. [Overview](#overview)
2. [Instructions](#instructions)
3. [MVP](#mvp)
4. [Next Steps](#next-steps)
5. [Task List](#task-list)


## Overview
This is an evidence-based app to help recommend skincare products and general skincare routines based on area of concern and ingredient safety. The app recommends products based on data analytics of user profiles, allowing users to filter for products that are reef-safe, pregnancy-safe, fragrance-free, etc. Users can start with a beginner-friendly skincare routine, and they can eventually level up to more advanced routines consisting of multiple steps and usage frequencies (per product or step) depending on active ingredients.


## Instructions
1. Setup virtual environment:
    * `virualenv env`
    * `source env/bin/activate`
    * `pip3 install -r requirements.txt`
2. Run seed_db.py:
    * `python3 seed_db.py` to use the default setup text file
    * `python3 seed_db.py some_kind_of_setup_file.txt` to use a preset setup text file
        * Note: You can create your own text file and follow the format of the default text file in `/data/file_list.txt`. Name it whatever you want, and use that name instead of `some_kind_of_setup_file.txt`.
3. View contents of database using PostgreSQL:
    * `psql project_test`

*Further steps to be added as project development progresses!*

*[Click here](#the-skincare-routine-helper) to go back to the top.*


## MVP:
- [x] (1) setup user login
    - 10/11: partially completed, but need to test implementation of flask-login extension to restrict views to logged-in (or logged-out) users
- [ ] (2) complete questionnaire for user profile
- [ ] (3) setup database with ingredients using Kaggle dataset
- [x] (4) search & display info for a product
    - 10/12: full product query will display now! time to work on the page for individual product details


## Next Steps
- [ ] request API keys
- [ ] test the server
- [ ] setup the homepage
- [ ] add product to user's cabinet
    - [ ] from product results list
    - [ ] from individual product details page
- [ ] queries, joins, etc.
- [ ] test product details page


## Task List
#### **General:**
- [ ] request API keys
- [ ] setup API calls in separate directory/layer
- [ ] request additional datasets (?)
- [x] 10/08: setup the server
- [ ] setup the homepage
- [x] 10/11: setup general navbar

#### **Data model:**
- [x] 10/06: create data models, [using dbdiagram.io](https://dbdiagram.io/)
- [x] 10/06: setup model.py
- [ ] add liked/disliked products for each user
    - [ ] sanitize comment section
- [ ] add irritation scores per ingredient and per product
    - [ ] could use Faker

#### **Setup database with actual data:**
- [ ] setup Kaggle dataset with clean ingredients (CSV file)
- [ ] setup other dataset
- [ ] look for datasets with sunscreen info

#### **Display information about a product:**
- [x] setup other json files
    - [x] 10/05: about_steps.json
    - [x] 10/05: skin_concerns.json
- [x] 10/11: setup product search results page
- [ ] setup individual product details page

#### **Complete questionnaire for user profile:**
- [ ] complete quick questionnaire for user profile
- [ ] setup questionnaire page
- [x] 10/11: setup user profile page
    - [x] 10/11: display user's cabinet, AM routine, and PM routine
- [ ] add products to user's cabinet, AM routine, and/or PM routine

#### **Setup search:**
- [ ] setup product search
    - [x] 10/09: lookup search tutorials
    - [x] 10/09: setup basic search using SQL queries
    - [x] 10/09: setup search using crud functions
    - [ ] test product search functions
- [ ] setup search page

#### **Testing:**
- [x] 10/09: setup test_crud.py
- [ ] test user login system
    - login, logout, restricted views
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
- [x] 10/06: test seeding the database for skin_concerns.json
    - [x] 10/06: seed_db.py
    - [x] 10/06: started crud.py
    - [x] 10/07: setup file to load CSV and JSON files into the database
- [x] 10/07: seed the database
    - [x] 10/07: products
    - [x] 10/07: ingredients
    - [x] 10/07: product_ingredients

#### **Setup user login:**
- [x] 10/08: setup login page
- [x] 10/08: setup new user registration page
    - [x] 10/09: confirm that this connects to the database
- [x] 10/11: setup user login system
    - [x] review: hashing passwords
    - [x] 10/09: setup basic login system
    - [x] 10/11: setup login system using flask-login
        - 10/11: had an issue where the terminal in VS code that was running my server crashed with this error message:
        - `The terminal process "/bin/bash" terminated with exit code: 1.`
        - Restarting VS code seemed fix it...??
    - [x] 10/11: setup logout function

*[Click here](#the-skincare-routine-helper) to go back to the top.*