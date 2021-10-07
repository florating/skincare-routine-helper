# THE SKINCARE ROUTINE HELPER
### Overview

This is an evidence-based app to help recommend skincare products and general routines based on area of concern and ingredient safety. The app recommends products based on data analytics of user profiles, allowing users to filter for products that are reef-safe, pregnancy-safe, fragrance-free, etc.

### Next Steps
- [ ] request API keys
- [ ] request dataset

**Setup database with ingredients:
- [ ] setup sample dataset
    - [x] 10/06: sample_products.csv: 2 dummy products with < 10 ingredients
    - [ ] generate sample_ingredients database and save somewhere
- [x] 10/06: test seeding the database for skin_concerns.json
    - [x] 10/06: seed_db.py
    - [x] 10/06: started crud.py
    - [ ] 10/07: setup file to load CSV and JSON files into the database
    - [ ] setup server.py

- [ ] seed the database
    - [ ] products
    - [ ] ingredients
    - [ ] product_ingredients

**Display information about a product:
- [x] setup other json files
    - [x] 10/05: about_steps.json
    - [x] 10/05: skin_concerns.json
- [ ] setup product display page

**Setup user login:
- [ ] setup user login system
    - [ ] review: hashing passwords
- [ ] setup login page
- [ ] setup new user registration page

**Complete questionnaire for user profile:
- [ ] complete quick questionnaire for user profile
- [ ] setup questionnaire page

**Setup search:
- [ ] setup search
    - [ ] lookup search tutorials
- [ ] setup search page


### Completed Steps
- [x] 10/06: create data models, [using dbdiagram.io](https://dbdiagram.io/)
- [x] 10/06: setup model.py