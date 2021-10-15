# THE SKINCARE ROUTINE HELPER

## Table Of Contents
1. [Overview](#overview)
2. [Instructions](#instructions)
3. [MVP](#mvp)
4. [Next Steps](#next-steps)
5. [Task List](#task-list)
6. [Journal](#journal)


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
- [x] (2) complete questionnaire for user profile
    - 10/13: completed! will add images later
- [x] (3) setup database with ingredients using Kaggle dataset
    - 10/12: completed! may need to migrate data from database to add TimestampMixin to the appropriate classes in model.py
- [x] (4) search & display info for a product
    - 10/12: routes for full product query and individual product details are now functioning and display information!


## Next Steps
- [ ] request API keys
- [ ] test the server
- [x] 10/09: setup a basic homepage
- [x] 10/14: add product to user's cabinet
    - [x] 10/14: from product results list
    - [ ] from individual product details page
- [ ] queries, joins, etc.
- [ ] test product details page


## Task List
#### **General:**
<details>

- [x] 10/08: setup the server
- [x] 10/11: setup general navbar (temporary)
- [ ] request API keys
- [ ] setup API calls in separate directory/layer
- [ ] request additional datasets (?)
- [ ] look into how to setup `login_manager.login_view`
</details>

#### **Data model:**
<details>

- [x] 10/06: create data models, [using dbdiagram.io](https://dbdiagram.io/)
- [x] 10/06: setup model.py
- [ ] add liked/disliked products for each user
    - [ ] sanitize comment section
- [ ] add irritation scores per ingredient and per product
    - [ ] could use Faker
- [ ] add ability to commit changes to name and email (user profile page)
</details>

#### **Setup database with actual data:**
<details>

- [x] 10/12: setup Kaggle dataset with clean ingredients (CSV file)
- [ ] setup other dataset
- [ ] look for datasets with sunscreen info
</details>

#### **Webpages:**
<details>

- [x] 10/09: setup basic homepage
    - [ ] reorganize
- [x] 10/13: setup user settings page
- [ ] add questionnaire page
- [ ] add library to learn more
    - [ ] skin types
    - [ ] skin concerns
</details>

#### **Cabinet and routine functionality:**
<details>

- [x] 10/11: display user's cabinet, AM routine, and PM routine
- [ ] add products to user's cabinet, AM routine, and/or PM routine
    - [x] 10/14: to cabinet from search results page
        - [ ] need to check if a the product already exists in the cabinet
</details>

#### **Complete questionnaire for user profile:**
<details>

- [x] 10/11: setup user profile page
- [x] 10/13: complete quick questionnaire for user profile within the settings page
- [ ] add descriptions and images to questionnaire
</details>

#### **Setup search:**
<details>

- [x] 10/11: setup search page
    - [x] 10/09: lookup search tutorials
    - [x] 10/09: setup basic search using SQL queries
    - [x] 10/09: setup search using crud functions
- [ ] maybe setup pagination or multiple queries with OFFSET and LIMIT parameters
    - [ ] setup better search by relevance
    - [x] 10/13: limit search results that are displayed using list concatenation
    - [x] 10/14: setup ability to use ORDER BY in the query
- [ ] consider livesearch options
    - [x] 10/14: setup `livesearch.js`, but need to serialize or jsonify data...
</details>

#### **Testing:**
<details>

- [x] 10/09: setup test_crud.py
- [ ] test user login system
    - login, logout, restricted views
- [ ] setup test_model.py
- [ ] setup test_server.py
- [ ] test product search functions
</details>


*[Click here](#the-skincare-routine-helper) to go back to the top.*

## Completed Steps

#### **Setup database with sample data:**
<details>

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
</details>

#### **Setup user login:**
<details>

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
</details>

#### **Display information about a product:**
<details>

- [x] 10/05: setup JSON and CSV files for sample dataset
    - [x] 10/05: files with general info:
        - about_steps.json
        - maybe more later?
    - [x] 10/05: files to seed db are listed in `/data/file_list.txt` or `/data/file_list_test2.txt`
- [x] 10/11: setup product search results page
- [x] 10/12: setup individual product details page
</details>


*[Click here](#the-skincare-routine-helper) to go back to the top.*

## Journal:

#### Thu, 10/14:
**HIGHLIGHT:** Added products to each user's cabinet! Downloaded [UNII codes](https://fdasis.nlm.nih.gov/srs/jsp/srs/uniiListDownload.jsp) for ingredient identification.
<details>

**accomplishments:**
- started working on AJAX with jQuery and React
- added a form and checkboxes to add multiple products into a user's cabinet from the product search results pages
    - need to check if the product already exists in the user's cabinet
- played around with livesearch.js
    - need to serialize things or jsonify to make this work, so this is in backlog
- added ability to modify product search query using ORDER BY, LIMIT

**blockers (somewhat resolved):**
- changed almost everything in models.py, so I will need to re-seed the database
    - `index_property`: added to data models for products, ingredients, am_routines, and pm_routines tables
    - `TimestampMixin`: added to all tables
    - `BaseQuery`: add to products table? to allow for pagination of results...
        - might already be built-in due to inheritance from `db.Model`
- will need a way to serialize results in order to use React to render results via AJAX
    - option 1: marshmallow on PyPI?
    - option 2: add `@property` to serialize ORM?
    - option 3: forget about it for now and do it the old fashioned way
- dataset has some irregularities (eg: duplicate ingredients in some products)
    - add UNII codes to ingredients table?

**questions:**
- should I use `pandas` to process CSV data to cross-reference the UNII codes that I downloaded?
- `pagination`? (maybe can't add to cabinet from there...)
- can I set a foreign key as an index property?
</details>

#### Wed, 10/13:
**HIGHLIGHT:** finished MVP!
<details>
    <summary>Click to expand!</summary>

**accomplishments:**
- setup user_settings.html template and route to the resource on the server
- complete quick questionnaire for user profile within the user settings page
    - not hard-coded in, so will update with new entries into the skintypes and concerns tables!
- limit the number of products displayed from a search using list concatenation in `server.py` for this route
- add a (non-functional) button to add to personal cabinet
    - TODO: use JS...?

**blockers (somewhat resolved):**
- `<div>` tag madness using classes for `flex-container`, `d-flex`, etc.
- deciding whether to add `TimestampMixin` to User and other tables in `model.py`.
    - will require data migration or re-seeding the db (manageable if done early on)
    - TODO: is it important to track date last updated? if so, schedule time to add this
- setting up general layout for `user_details.html`, `profile_settings.html`, and `product_details.html` using `<div class="col-#">`

**refactoring:**
    - added `{% block after_body %}{% endblock %}` to the end of all 6 HTML templates that extend `base.html`
    - deleted `products.html` because it is not being used (actually using `product_details.html`)
</details>


#### Tue, 10/12:

**HIGHLIGHT:** nearly finished MVP!
<details>
<summary>Click to expand!</summary>

**accomplishments:**
- updated Product constructor function, which calls Ingredient and ProductIngredient constructor functions from `crud.py`
    - checks for duplicate products and ingredient
    - TODO: check for duplicate entries in ingredients list... some products have ingredient lists with repeated items!!
        - eg: CeraVe Moisturising Cream 50ml has "cetearyl alcohol" repeated 2x
- things are talking from front-end to back-end!

**yesterday's blockers (resolved!):**
- VS code error (`exit code: 1`)
- could not import `flask_login`, but was bc of env

**questions:**
- use `cascade` vs `onUpdate` vs something else for models when updating assignments?
- how to add Trello card-like elements for routines/cabinet, such that they can snap into position?

**project goal:**
- setup data visualization for:
    - possible allergens per user
    - brands with cleaner ingredients
- help people level up skincare routine
- filters for products:
    - cruelty-free
    - vegan
    - recommended for specific skintypes
- filter for brands:
    - parse brand names from product names
    - black-owned business
    - no recent scandals..??

Note: I keep comitting to my repo starting with `Refactor code` and I could probably be more descriptive... Unless it's actually just a minor change.
</details>

*[Click here](#the-skincare-routine-helper) to go back to the top.*
