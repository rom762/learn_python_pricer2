from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    remember_me = BooleanField('Remember me', default=True, render_kw={"class": "form-check-input"})
    submit = SubmitField('Login', render_kw={"class": "btn btn-primary"})


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"class": "form-control"})
    firstname = StringField('Firstname', validators=[DataRequired()], render_kw={"class": "form-control"})
    lastname = StringField('Lastname', validators=[DataRequired()], render_kw={"class": "form-control"})
    city = StringField('City', validators=[DataRequired()], render_kw={"class": "form-control"})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Sign In', render_kw={"class": "btn btn-primary"})



    def __str__(self):
        return str(self.email.value) + str(self.firstname.value)