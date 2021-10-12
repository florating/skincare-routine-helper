"""Server for the skincare routine helper."""
# import os

from flask import flash, Flask, redirect, render_template, request, session, url_for
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

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = ""

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
    # FIXME: need to clear session or use flask-login to logout_user()
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


@app.route('/products/<int:product_id>')
def show_product(product_id):
    """Show product profile for a particular product."""

    product_obj = crud.get_obj_by_id('Product', escape(product_id))
    return render_template('product_details.html', product=product_obj)


@app.route('/products', methods=['GET'])
def show_all_products(product_list):
    return render_template('products.html', product_list=product_list)


@app.route('/search', methods=['GET'])
def show_products_from_search():
    # form.serialize()
    params = {
        'product_name': request.args.get('product_name'),
        'product_type': request.args.get('product_type'),
    }
    # product_results = model.Product.query.filter(model.Product.product_name.like(f'%{params["product_name"]}%')).all()
    print(f'params["product_type"] = {params["product_type"]}')

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
    product_query = model.Product.query
    for param, param_val in params.items():
        if param_val:
            # for exact match
            product_query = product_query.filter_by({param: param_val})
            # FIXME: add code for partial matches, lowercase, etc.
    result = product_query.all()

    return redirect(url_for('show_all_products', product_list=result))


if __name__ == '__main__':
    print("Hello, I'm in server.py's special statement since __name__ == '__main__'!")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)