import logging
from pprint import pprint
from .forms import MultiCheckboxField, ShopsChoiceForm
from flask import (Blueprint, current_app, flash, redirect,
                   render_template, url_for, request)
from webapp.model import db, Shop
from .parsers.parse_citilink import parse_citilink
from .parsers.parse_regard import parse_regard
blueprint = Blueprint('parse', __name__, template_folder='templates',
                      url_prefix='/parse')
from flask_login import login_required

@blueprint.route('/', methods=['POST', 'GET'])
@login_required
def parse_it():
    title = 'Let\'s parse!'
    parse_functions = {
        'citilink' : parse_citilink,
        'regard': parse_regard,
    }
    form = ShopsChoiceForm()
    if form.validate_on_submit():
        print(form.example.data)
        flash('Form Validated!', 'success')
        shops = Shop.query.filter(Shop.name.in_(form.example.data))
        shop_list = [shop.name for shop in shops]
        for shop in shop_list:
            current_parse_function = parse_functions[shop]
            result = current_parse_function()
            if result:
                flash(result['message'], result['status'] )

        print(f'all shops: {shop_list}')
        return render_template("success.html", data=shop_list,
                               page_title='Success', menu=current_app.menu)
    else:
        print("Validation Failed")
        print(form.errors)

    return render_template('parse.html', page_title=title,
                           menu=current_app.menu, form=form)


