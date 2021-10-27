"""Server routes and view functions."""

from flask import flash, Flask, jsonify, redirect, render_template, request, session, url_for
import flask_login
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from jinja2 import StrictUndefined
from markupsafe import escape
from werkzeug.security import check_password_hash

from database import crud
from database import model
from database.model import db, connect_to_db

print(f"Hello, I'm in server.py and __name__ = {__name__}!")

app = Flask(__name__)
app.secret_key = 'secret'
# FIXME: set app configurations for SECRET_KEY later, after fixing secrets.sh
# SECRET_KEY = os.environ['SECRET_KEY']

app.jinja_env.undefined = StrictUndefined

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in or register for an account first.'


@app.route('/')
def show_index():
    # TODO: read db_summary.csv file instead of calculating db_counts
    # db_counts = crud.get_summary_prod_table()
    return render_template('index.html')


@login_manager.user_loader
def load_user(user_id):
    """This callback is used to reload the user object from the user ID (in unicode) stored in the session.
    
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
    
    # FIXME: not yet tested. is it better to call generate_password_hash here or in model.py?
    crud.create_user(**params)
    flash('Thank you for creating a new account! Please log in.')
    return redirect('/')
    

@app.route('/login', methods=['GET', 'POST'])
def login():
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
            login_user(user)
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
    # session.clear()
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
                    current_user.skintype_id = val
                elif 'primary_concern_id' in param:
                    current_user.primary_concern_id = val
                elif 'secondary_concern_id' in param:
                    current_user.secondary_concern_id = val
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


@app.route('/livesearch', methods=['GET', 'POST'])
def livesearch():
    """GET: display page; POST: perform a search as the user types into the search box
    Uses jQuery and AJAX with SQLAlchemy queries.
    """

    if request.method == 'POST':
        search_text = request.form.get('text')
        search_order_by = request.form.get('order_by')
        search_limit = 10  # can change this later
        
        # TODO: sanitize user input in search_text
        q = model.Product.query.filter(
            model.Product.product_name.ilike(f'%{search_text}%')
            ).order_by(search_order_by).limit(search_limit)
        
        result = q.first_or_404()
        if result != 404:
            ser_obj = result.serialize
        return jsonify(ser_obj)
        else:
            return result

    return render_template('livesearch.html')
    # eg: result =
    # (1, 'The Ordinary Natural Moisturising Factors + HA', None, 'https://www.lookfantastic.com/the-ordinary-natural-moisturising-factors-ha-30ml/11396687.html', '30ml', '£5.20', None, 1, None, datetime.datetime(2021, 10, 15, 21, 31, 19, 813822, tzinfo=datetime.timezone.utc))
    # return jsonify(json_list=result.serialize)


@app.route('/products', methods=['GET', 'POST'])
def show_products_from_search():
    """Search for skincare products in the database.

    Use form data from /products (in 'search-form.html') to populate any search parameters.
    """
    if request.method == 'POST':
        param_list = ['product_name', 'category_id', 'order_by']
        form_params = crud.process_form(param_list, request.form)
        form_params.update({'limit': 10})

        q = model.Product.query
        for param, param_val in form_params.items():
            # print(f"for param = {param} and param_val = {param_val}\n\n")
            if param_val:
                if param == 'product_name':
                    q = q.filter(model.Product.product_name.ilike(f'%{param_val}%'))
                elif param == 'category_id':
                    q = q.filter(model.Product.category_id == int(param_val))
                    # TODO: add ability to check multiple product types in a single search query
                elif param == 'order_by':
                    # print(f"param_val = {param_val}\n\n\n")
                    q = q.order_by(param_val)
                elif param == 'limit':
                    q = q.limit(param_val)

        # print(f"q = {q}\n\n\n")
        result = q.all()

        if current_user.is_anonymous:
            cab_prod_id_list = ''
            return render_template('search-results-noauth.html', product_list=result)
        # cab_prod_id_list = []
        # for cab_obj in current_user.cabinets:
        #     cab_prod_id_list.append(cab_obj.product_id)
        cab_prod_id_list = current_user.serialize_cabinet_prod_ids

        return render_template('search-results.html',
            product_list=result, current_cabinet=cab_prod_id_list)

    return render_template('search-form.html', categories_table = model.Category.query.all())


@app.route('/add_to_cabinet', methods=['POST'])
@login_required
def add_products_to_cabinet():
    data_pojo = request.form
    p_id_list = data_pojo.to_dict(flat=False)['product_id']

    # This works for 1 or more product_ids in the data_pojo.
    for p_id in p_id_list:
        # FIXME: check if this product_id is already in this user's cabinet (any option?)
        # model.Cabinet.query.filter_by(user_id=session['_user_id']).filter_by(product_id=p_id)
        # user_cabinet_list = current_user.cabinets
        # current_user.serialize_cabinets

        obj = model.Cabinet(user_id=current_user.get_id(), product_id=p_id)
        db.session.add(obj)

    db.session.commit()
    flash("You successfully added these products to your cabinet!")
    return redirect(url_for('show_profile'))


@app.route('/get_cabinet', methods=['POST'])
@login_required
def get_cabinet_list():
    """Return a list of products within a user's cabinet to send to routines.js."""

    cat_dict = [crud.get_category_dict()]
    cabs = current_user.serialize_cabinets
    return jsonify(cat_dict = cat_dict, cabinet = cabs)


@app.route('/routine', methods=['GET', 'POST'])
def setup_routine():
    """
    NOTE: request.form looks like this:
        ImmutableMultiDict([
            ('routine_type', 'am'),
            ('steps[0][category_id]', '1'),
            ('steps[0][product_id]', '64')
        ])
    NOTE: request.form.to_dict(flat=False) looks like this:
        {'routine_type': ['am'], 'steps[0][category_id]': ['1'], 'steps[0][product_id]': ['64']}
    NOTE: request.form.to_dict(flat=True) looks like this:
        {'routine_type': 'am', 'steps[0][category_id]': '1', 'steps[0][product_id]': '64'}
    """
    if request.method == 'POST':
        data = request.form
        print(data)
        
        am_or_pm = request.form.get("routine_type")
        form_dict = request.form.to_dict(flat=True)
        print("form_dict is...")
        print(form_dict)

        steps_dict = form_dict['steps'][0]
        print("steps_dict is...")
        print(steps_dict)

        print(f'\n\n\nCreating a new {am_or_pm.upper()} routine:')
        for cat_id, p_id in steps_dict.items():
            category_name = model.Category.query.filter_by(
                category_id=cat_id).first().category_name
            print(f'\n\n{category_name} step with cat_id = {cat_id}')
            print(f'p_id = {p_id}')
            p_obj = crud.get_obj_by_id('Product', p_id)  # change p_id to int?
            print('\n\n\np_obj is:')
            print(p_obj)
        
        print("We went to /routine with a POST request successfully!")
        return "Success!"
    return render_template('test/routine_blank.html')


@app.route('/routine_blank')
def setup_routine_blank():
    return render_template('test/routine_blank.html')


@app.route('/test')
def test_react():
    test_obj = crud.get_obj_by_id('Product', 1)
    print('\n\n\n test_obj')
    print(test_obj)
    return render_template('test/test_transition.html')


if __name__ == '__main__':
    print("Hello, I'm in server.py's special statement since __name__ == '__main__'!")
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)
