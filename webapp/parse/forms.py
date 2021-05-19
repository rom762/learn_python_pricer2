from pprint import pprint

from flask import current_app
from flask_wtf import FlaskForm
from wtforms import widgets, SubmitField, HiddenField, SelectMultipleField
from webapp.model import db, Shop


class ParseForm(FlaskForm):
    shops = ['one', 'two']
    submit = SubmitField('Parse', render_kw={"class": "btn btn-primary"})


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class SimpleForm(FlaskForm):
    list_of_files = ['citilink', 'regard']
    print(f'list_of_files: {list_of_files}, {type(list_of_files)}')
    # create a list of value/description tuples
    shops = [(x, x) for x in list_of_files]
    print(f'files: {shops}')
    example = MultiCheckboxField('Label', choices=shops)
