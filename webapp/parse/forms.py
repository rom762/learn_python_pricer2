from pprint import pprint

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import widgets, SubmitField, HiddenField, SelectMultipleField
from webapp.model import db, Shop


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class ShopsChoiceForm(FlaskForm):
    list_of_shops = ['citilink', 'regard']
    print(f'list_of_files: {list_of_shops}, {type(list_of_shops)}')
    # create a list of value/description tuples
    shops = [(x, x) for x in list_of_shops]
    print(f'files: {shops}')
    example = MultiCheckboxField('Label', choices=shops)
