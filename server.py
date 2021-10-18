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
            return redirect(url_for('show_profile'))
        
        flash(error)
        return redirect('/')
    else:
        flash("You are not using a POST request.")
        return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


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
    # use SQLAlchemy queries

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
    # eg: result =
    # (1, 'The Ordinary Natural Moisturising Factors + HA', None, 'https://www.lookfantastic.com/the-ordinary-natural-moisturising-factors-ha-30ml/11396687.html', '30ml', '£5.20', None, 1, None, datetime.datetime(2021, 10, 15, 21, 31, 19, 813822, tzinfo=datetime.timezone.utc))

    # return jsonify(json_list=result.serialize)


@app.route('/products/search', methods=['POST'])
def show_products_from_search():
    """Search for skincare products in the database.

    Use form data from /products (in 'search_form.html') to populate any search parameters.
    # FIXME: pick one of the following ways to implement search...
    
    # Option 1:
    # product_results = crud.get_all_obj_by_param('Product', **params)
    
    # Option 2:
    # sql = "SELECT product_id, product_name FROM products WHERE product_name = :product_name"
    # cursor = db.session.execute(sql, **params)
    # result = cursor.fetchall()
    
    # Option 3:
    # check if product_name exists, then can add a filter
    # if other params exist, then add those
    """

    form_params = {
        'product_name': request.form.get('product_name', ''),
        'order_by': request.form.get('order_by', ''),
        # 'product_type': request.form.get('product_type', ''),
        'category_id': request.form.get('category_id', ''),
        'limit': 10
    }

    q = model.Product.query
    print("ABOUT TO START FOR LOOP!\n\n\n")
    for param, param_val in form_params.items():
        print(f"for param = {param} and param_val = {param_val}\n\n")
        if param_val:
            print(f"I'M IN LINE 277!")
            if param == 'product_name':
                q = q.filter(model.Product.product_name.ilike(f'%{param_val}%'))
            # FIXME: no product types allowed...
            elif param == 'category_id':
                q = q.filter(model.Product.category_id == int(param_val))
                #   .in_(param_val)
            # TODO: add order_by and limit functionality for the search
            elif param == 'order_by':
                print(f"param_val = {param_val}\n\n\n")
                q = q.order_by(param_val)
            elif param == 'limit':
                q = q.limit(param_val)

    print(f"q = {q}\n\n\n")
    result = q.all()

    cab_prod_id_list = []
    for cab_obj in flask_login.current_user.cabinets:
        cab_prod_id_list.append(cab_obj.product_id)

    return render_template('search-results.html', product_list=result, current_cabinet=cab_prod_id_list)


@app.route('/add_to_cabinet', methods=['POST'])
def add_products_to_cabinet():
    
    # print(f"type(data_pojo) = {type(data_pojo)}")
    # print(f"data_pojo.to_dict(flat=False) = {data_pojo.to_dict(flat=False)}")

    # NOTE: not in for loop... data_pojo = ImmutableMultiDict([('product_id', '75'), ('product_id', '342')])
    # NOTE: type(data_pojo) = <class 'werkzeug.datastructures.ImmutableMultiDict'>
    # NOTE: data_pojo.to_dict(flat=False) = {'product_id': ['75', '342']}
    data_pojo = request.form
    print(f"NOTE: not in for loop... data_pojo = {data_pojo}")

    p_id_list = data_pojo.to_dict(flat=False)['product_id']

    # This works for 1 or more product_ids in the data_pojo.
    for p_id in p_id_list:
        print(f"\n\n\nNOTE: we in the for loop yoooo... p_id_list = {p_id_list}\n\n\n")
        print(f"YO YO YO: the session is {session}\n\n\n")
        print(f"session.get('user_id') = {session.get('user_id')}\n\n\n")

        # check if this product_id is already in this user's cabinet
        model.Cabinet.query.filter_by(user_id=session['_user_id'])
        # filter_by(product_id... using in_?)

        user_cabinet_list = flask_login.current_user.cabinets
        print(f"user_cabinet_list = {user_cabinet_list}\n\n\n")

        obj = model.Cabinet(
            user_id=session['_user_id'],
            product_id=p_id
        )
        print(f"I just created a Cabinet obj = {obj}\n\n\n")
        print(f"Its product_id is {obj.product_id}\n\n\n")
        db.session.add(obj)

    print("I'm out of the for loop and tried to add things to the cabinet!\n\n\n")
    db.session.commit()
    flash("You successfully added these products to your cabinet!")
    print("We got to line 283! Hopefully that's good news!\n\n\n")
    print(f"user_cabinet_list = {user_cabinet_list}\n\n\n")
    return redirect(url_for('show_profile'))


@app.route('/routine')
def setup_routine():
    return render_template('routine.html')


if __name__ == '__main__':
    print("Hello, I'm in server.py's special statement since __name__ == '__main__'!")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
