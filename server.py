"""Server for the skincare routine helper."""
# import os

from flask import flash, Flask, jsonify, redirect, render_template, request, session, url_for
import flask_login
from flask_login import LoginManager, login_required, login_user, logout_user
from jinja2 import StrictUndefined
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash

import crud
import model
from model import db, connect_to_db

print(f"Hello, I'm in server.py and __name__ = {__name__}!")

app = Flask(__name__)
app.secret_key = 'secret'
# FIXME: set app configurations for SECRET_KEY later, after fixing secrets.sh
# SECRET_KEY = os.environ['SECRET_KEY']

app.jinja_env.undefined = StrictUndefined

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ""   # FIXME: not setup yet, may need extra views as well


@app.route('/')
def show_index():
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    """This callback is used to reload the user object from the user ID stored in the session.
    
    It should take the unicode ID of a user, and return the corresponding user object.
    
    If the ID is not valid, it should return None (not raise an exception). In that case, the ID will manually be removed from the session and processing will continue.
    """
    return model.User.query.get(user_id)


@app.route('/register', methods=['POST'])
def register_account():
    """Register a new account."""

    params = {
        'f_name': request.form.get('f_name'),
        'l_name': request.form.get('l_name'),
        'email': request.form.get('email'),
        'password': request.form.get('password')  # will be hashed in crud
    }
    
    user = crud.get_user_by_email(params['email'])

    if user:
        flash('You cannot use this email to create a new account.')
        return redirect('/')
    
    # FIXME: not yet complete nor tested
    # serialize? is it better to call generate_password_hash here or in model.py?
    crud.create_user(**params)
    flash('Thank you for creating a new account! Please log in.')
    return redirect('/')
    

@app.route('/login', methods=['GET', 'POST'])
def process_login():
    """Process user login."""

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        error = None
        user = crud.get_user_by_email(email)

        if not user:
            error = 'Incorrect email address.'  # FIXME: specificity is for tests only
        elif not user.check_password(password):
            error = 'Incorrect password.'   # FIXME: specificity is for tests only
            # flash('Your login credentials are incorrect.')
        
        if error is None:
            # FIXME: not completed yet, may create new function in User class
            # Also will beef up security! Someone could look at the cookies...
            login_user(user)
            # session.clear()
            # session['user_email'] = user.email

            flash('Welcome, you have successfully logged in.')
            return redirect(url_for('show_user', user_id=user.user_id))
        
        flash(error)
        return redirect('/')
    else:
        flash(error)
        return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/users/<user_id>')
@login_required
def show_user(user_id):
    """Show user profile for a particular user."""

    user_obj = crud.get_obj_by_id('User', escape(user_id))
    return render_template('user_details.html', user=user_obj)


@app.route('/user_profile')
@login_required
def show_profile():
    return render_template('user_details.html')


@app.route('/settings')
@login_required
def show_profile_settings():
    concerns = model.Concern.query.all()
    skintypes = model.Skintype.query.all()

    return render_template('profile_settings.html', concerns=concerns, skintypes=skintypes)


@app.route('/quiz', methods=['POST'])
@login_required
def update_skin_profile():
    params = ['skintype_id', 'primary_concern_id', 'secondary_concern_id']
    try:
        for param in params:
            val = request.form.get(param)
            if val:
                if 'skintype_id' in param:
                    flask_login.current_user.skintype_id = val
                elif 'primary_concern_id' in param:
                    flask_login.current_user.primary_concern_id = val
                elif 'secondary_concern_id' in param:
                    flask_login.current_user.secondary_concern_id = val
        db.session.commit()
        flash('You have successfully updated your skin profile!')
    except:
        db.session.rollback()
        flash('Something did not work...')
    return redirect('/settings')


@app.route('/products/<product_id>')
def show_product(product_id):
    """Show product profile for a particular product."""

    product_obj = model.Product.query.get(escape(product_id))
    print(product_obj.product_name)
    return render_template('product_details.html', product=product_obj)


@app.route('/products', methods=['GET'])
def show_all_products():
    return render_template('search_form.html', categories_table = model.Category.query.all())


@app.route('/test')
def test_search():
    return render_template('livesearch.html')


@app.route('/livesearch', methods=['POST', 'GET'])
def livesearch():
    """Perform a search as the user types into the searchbox.
    Uses jQuery and AJAX.
    """
    sql_query = "SELECT * FROM products WHERE product_name LIKE :product_name LIMIT :limit"
    #  ORDER BY :order_by LIMIT :limit"
    params = {
        'product_name': "%" + request.form.get('text') + "%",
        'order_by': request.form.get('order_by'),
        'limit': 10
    }
    # To protect against SQL injection attacks, use SQLAlchemy's
    # built-in parameter substitution.
    cursor = db.session.execute(sql_query, params)
    result = cursor.fetchone()
    print(f"result = {result}")
    return result


@app.route('/products/search', methods=['POST'])
def show_products_from_search():
    """Search for skincare products in the database.

    Use form data from /products (in 'search_form.html') to populate any search parameters.
    """

    # form_params = request.form.to_dict(flat=False)
    # form_params = normal dict (flattened ImmutableMultiDict)

    form_params = {
        'product_name': request.form.get('product_name', ''),
        'order_by': request.form.get('order_by', ''),
        # 'category_id': request.form.get('category_id', ''),
        'limit': 10
    }


    print("\n\n\n")
    print(f"request.form = {request.form}")
    # request.form = ImmutableMultiDict(
    #   [
    #       ('product_name', 'lotion'),
    #       ('order_by', 'product_name'),
    #       ('category_id', '1'),
    #       ('category_id', '2')
    #   ]
    # )

    print("\n\n\n")
    print(f"form_params = {form_params}\n\n\n")
    # form_params = {
    #   'product_name': ['lotion'],
    #   'order_by': ['product_name'],
    #   'category_id': ['1', '2']
    # }

    # Handle the user input for the checkboxes in for category_id separately:
    # cat_id_list_length = len(form_params.pop('category_id', None))

    # test_retrieval_list = request.form.getlist('category_id')

    # print(f"cat_id_list_length = {cat_id_list_length}\n\n\n")
    # i = 0
    # payload['category_id'] = []
    # while i < cat_id_list_length:
    #     test_thing = request.form.get('category_id', type=int)
    #     print(f"test_thing = {test_thing}\n\n\n")
    #     payload['category_id'].append(test_thing)
    #     i += 1
    # for i, cat_id_str in enumerate(cat_id_list):
    #     cat_id_list[i] = int(cat_id_str)
    # payload['category_id'] = cat_id_list

    # FIXME: pick one of the following ways to implement search...
    # FIXME: and also need to remove search parameters if form is empty
    
    # Option 1:
    # product_results = crud.get_all_obj_by_param('Product', **params)
    
    # Option 2:
    # sql = "SELECT product_id, product_name FROM products WHERE product_name = :product_name"
    # cursor = db.session.execute(sql, **params)
    # result = cursor.fetchall()
    
    # Option 3:
    # check if product_name exists, then can add a filter
    # if other params exist, then add those
    q = model.Product.query
    print("ABOUT TO START FOR LOOP!\n\n\n")
    for param, param_val in form_params.items():
        print(f"for param = {param} and param_val = {param_val}\n\n")
        if param_val:
            print(f"I'M IN LINE 277!")
            if param == 'product_name':
                q = q.filter(model.Product.product_name.ilike(f'%{param_val}%'))
            # FIXME: no product types allowed...
            # elif param == 'category_id':
            #     q = q.filter(
            #       model.Product
            #       .category_id
            #       .in_(param_val)
            #     )
            # TODO: add order_by and limit functionality for the search
            elif param == 'order_by':
                print(f"param_val = {param_val}\n\n\n")
                q = q.order_by(param_val)
            elif param == 'limit':
                q = q.limit(param_val)
    print(f"q = {q}\n\n\n")
    result = q.all()

    return render_template('search-results.html', product_list=result)


@app.route('/add_to_cabinet', methods=['POST'])
def add_products_to_cabinet():
    data_pojo = request.form
    print(f"NOTE: not in for loop... data_pojo = {data_pojo}")
    # print(f"type(data_pojo) = {type(data_pojo)}")
    # print(f"data_pojo.to_dict(flat=False) = {data_pojo.to_dict(flat=False)}")

    # NOTE: not in for loop... data_pojo = ImmutableMultiDict([('product_id', '75'), ('product_id', '342')])
    # NOTE: type(data_pojo) = <class 'werkzeug.datastructures.ImmutableMultiDict'>
    # NOTE: data_pojo.to_dict(flat=False) = {'product_id': ['75', '342']}
    p_id_list = data_pojo.to_dict(flat=False)['product_id']
    for p_id in p_id_list:
        print(f"NOTE: we in the for loop yoooo... p_id_list = {p_id_list}")
        print(f"YO YO YO: the session is {session}")
        print(f"session.get('user_id') = {session.get('user_id')}")
        obj = model.Cabinet(
            user_id=session['_user_id'],
            product_id=p_id
        )
        print(f"I just created a Cabinet obj = {obj}")
        print(f"Its product_id is {obj.product_id}")
    print("I tried to add things to the cabinet!")
    flash("You successfully added these products to your cabinet!")
    return 'Hello'  # shouldn't happen...


if __name__ == '__main__':
    print("Hello, I'm in server.py's special statement since __name__ == '__main__'!")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)