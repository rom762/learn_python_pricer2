from flask import Blueprint
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, url_prefix='/users')


menu = {
        'Home': '/',
        'GPU': '/gpu',
        'News': '/news',
        'Weather': '/weather',
        'Register': '/register',
        'Login': '/login',
        'Profile': '/profile',
    }


@blueprint.route('/login')
def login():
    print(f'url for login: {url_for("login")}')
    if current_user.is_authenticated:
        flash('You are logged in', 'success')
        return redirect(url_for('index'))
    title = 'Login'
    login_form = LoginForm()
    return render_template('login.html', title=title, menu=menu, form=login_form)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user, remember=login_form.remember_me.data)
            flash('You are logged in', 'success')
            return redirect(url_for('gpu'))
    flash('Неправильное имя пользователя или пароль', 'warning')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
@login_required
def logout():
    flash('You are logged out.', 'primary')
    logout_user()
    return redirect(url_for('user.login'))