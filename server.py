"""Server routes and view functions."""

import json
import os
from pprint import pprint

from flask import flash, Flask, jsonify, redirect, render_template, request, session, url_for
from flask_login import current_user, LoginManager, login_required, login_user, logout_user
from jinja2 import StrictUndefined
from markupsafe import escape
from werkzeug.security import check_password_hash

from database import crud
from database import model
from database.model import db, connect_to_db

app = Flask(__name__)

# FIXME: the following bits of code are for testing purposes only!
# set app configurations for SECRET_KEY later, after fixing secrets.sh
_SECRET_KEY = os.environ.get('SECRET_KEY', 'secret')
# print(_SECRET_KEY)
app.secret_key = _SECRET_KEY

_DB_NAME_ = 'project_test_2'

app.jinja_env.undefined = StrictUndefined

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in or register for an account first.'


@app.route('/')
def index():
    # NOTE: js reads db_summary.csv file instead of crud calculating it
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
        return redirect(url_for('home'))
    
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
    return render_template('login.html')
    # return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    # session.clear()
    return redirect('/')


@app.route('/user_profile')
@login_required
def show_profile():
    am_r, pm_r = None, None
    routine_ids = [am_r, pm_r]
    routines_to_show = {}
    # TODO: add am_r_obj and pm_r_obj to routines_to_show
    print('Show current_user.routines...')
    print(current_user.routines)
    for routine in current_user.routines:
        am_r = routine.routine_id if routine.am_or_pm == 'am' else None
        pm_r = routine.routine_id if routine.am_or_pm == 'pm' else None
    for r_id in routine_ids:
        if r_id:
            routines_to_show['am_r'] = crud.get_obj_by_id('Routine', r_id)
    return render_template('user_details.html', am_routine=am_r, pm_routine=pm_r)


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

        QUERY = model.Product.query
        for param, param_val in form_params.items():
            # print(f"for param = {param} and param_val = {param_val}\n\n")
            if param_val:
                if param == 'product_name':
                    QUERY = QUERY.filter(model.Product.product_name.ilike(f'%{param_val}%'))
                elif param == 'category_id':
                    QUERY = QUERY.filter(model.Product.category_id == int(param_val))
                    # TODO: add ability to check multiple product types in a single search query
                elif param == 'order_by':
                    # print(f"param_val = {param_val}\n\n\n")
                    QUERY = QUERY.order_by(param_val)
                elif param == 'limit':
                    QUERY = QUERY.limit(param_val)

        # print(f"QUERY = {QUERY}\n\n\n")
        result = QUERY.all()

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

    try:
        db.session.commit()
        flash("You successfully added these products to your cabinet!")
    except:
        # FIXME: need an exception...
        db.session.rollback()
        flash('Something did not work...')
    return redirect(url_for('show_profile'))


@app.route('/get_cabinet', methods=['POST'])
@login_required
def get_cabinet_list():
    """Return a list of products within a user's cabinet to send to routines.js."""
    # TODO: check if GET request url still shows up via AJAX with routines.js
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
        # ImmutableMultiDict([('{"routine_type":"am","steps":["88","559"]}', '')])
            # request.form.to_dict(flat=True) is...
            # {'{"routine_type":"am","steps":["88","559"]}': ''}

        am_or_pm = request.form.get("routine_type")  # 'am' or 'pm'
        # pprint(am_or_pm)
        # routine_id = request.form.get("routine_id")  # TODO: add to routines.js
        form_dict = request.form.to_dict(flat=False)
        # print("request.form.to_dict(flat=False) is...")
        # pprint(form_dict)
        routine_type = form_dict['routine_type']  # am or pm
        steps = form_dict['steps[]']
        # pprint('Printing routine_type and steps from form_dict now...')
        # pprint(routine_type)
        # pprint(steps)
        # if not routine_id:
        routine_obj = model.Routine(user=current_user, am_or_pm=am_or_pm)
        print(routine_obj)
        # else:
        #     routine_obj = crud.get_obj_by_id('Routine', routine_id)
        step_list = []
        for prod_id in steps:
            step_obj = model.Step(product_id=prod_id)
            step_list.append(step_obj)
            print(step_obj)
        routine_obj.steps = step_list
        print(routine_obj)
        # NOTE: final version!
            # form_data from routines.js = {
            #   'routine_type': 'am',
            #   'steps[]': '559'
            # }
            # 'jsonify(request.form) is...'
            #   <Response 48 bytes [200 OK]>
            # request.form.to_dict(flat=False) is...
            #   {'routine_type': ['am'], 'steps[]': ['559', '88']}
            # 'Printing routine_type and steps from form_dict now...'
                # routine_type = form_dict['routine_type'] --> ['am']
                # steps = form_dict['steps[]'] --> ['559', '88']
        print('We went to /routine with a POST request successfully!')
        db.session.add(routine_obj)
        db.session.commit()
        print(f'This routine ({routine_obj.routine_id}) has been added to the database.')
        pprint(routine_obj.serialize)
        pprint(routine_obj.serialize_current_steps)
        pprint(routine_obj.serialize_current_steps_verbose)
        return 'Success!'
    # TODO: retrieve and send the user's active AM and PM routines
    am_routine = crud.get_obj_by_id('Routine', current_user.am_routine_id)
    pm_routine = crud.get_obj_by_id('Routine', current_user.pm_routine_id)
    return render_template('routine_blank.html', am_routine=am_routine, pm_routine=pm_routine)


@app.route('/add/routine', methods=['POST'])
@login_required
def add_routine():
    form_data = {
        'am_or_pm': request.form.get('routine_type'),
        'name': request.form.get('name'),
        'user': current_user
    }
    routine_obj = crud.create_table_obj('Routine', **form_data)
    return routine_obj.routine_id


@app.route('/test/semantic')
def test_semantic():
    return render_template('base_semantic.html')


@app.route('/test')
def test_react():
    test_obj = current_user.serialize_for_profile
    test_2 = current_user.serialize_routines
    test_3 = current_user.serialize_active_routines
    print('\n\n\n test_obj')
    print(test_obj)
    print('\n\n\n current_user.serialize_routines')
    print(test_2)
    print('\n\n\n current_user.serialize_active_routines')
    print(test_3)
    print('\n\n\n')

    print(current_user.primary_concern)
    return render_template('modal_routine.html')


if __name__ == '__main__':
    print("Hello, I'm in server.py's special statement since __name__ == '__main__'!")
    connect_to_db(app, db_uri=f"postgresql:///{_DB_NAME_}", echo=False)
    db.create_all()
    app.run(host='0.0.0.0', debug=True)
