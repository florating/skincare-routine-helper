"""Server for the skincare routine helper."""
# import os

from flask import flash, Flask, redirect, render_template, request, session, url_for
from jinja2 import StrictUndefined
from werkzeug.security import generate_password_hash, check_password_hash

import crud
import model
from model import db, connect_to_db

print(f"Hello, I'm in server.py and __name__ = {__name__}!")

app = Flask(__name__)

# SECRET_KEY = os.environ['SECRET_KEY']
# FIXME: set app configurations for SECRET_KEY later, after fixing secrets.sh
app.secret_key = 'secret'
app.jinja_env.undefined = StrictUndefined
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def show_index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register_account():
    """Register a new account."""

    f_name = request.form.get('f_name')
    l_name = request.form.get('l_name')
    email = request.form.get('email')
    password = request.form.get('password')
    user = model.User.query.filter_by(email=email).first()

    if user:
        flash('You cannot use this email to create a new account.')
        return redirect('/')
    
    # FIXME: not yet complete nor tested
    # serialize? is it better to call generate_password_hash here or in model.py?
    new_user = model.User(
        email=email,
        password=generate_password_hash(password, method='sha256'),
        f_name=f_name, 
        l_name=l_name)
    db.session.add(new_user)
    db.session.commit()
    flash('Thank you for creating a new account! Please log in.')
    return redirect('/')
    

@app.route('/login', methods=['POST'])
def process_login():
    """Process user login."""

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
        session.clear()
        session['user_email'] = user.email
        flash('Welcome, you have successfully logged in.')
        return redirect(url_for('/users', user_id=user.user_id))
    
    flash(error)
    return redirect('/')


@app.route('/users/<user_id>')
def show_user(user_id):
    """Show user profile for a particular user."""

    user_obj = crud.get_obj_by_id('User', user_id)
    return render_template('user_details.html', user=user_obj)


@app.route('/products/<product_id>')
def show_product(product_id):
    """Show product profile for a particular product."""

    product_obj = crud.get_obj_by_id('Product', product_id)
    return render_template('product_details.html', product=product_obj)


if __name__ == '__main__':
    print("Hello, I'm in server.py's special statement since __name__ == '__main__'!")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)