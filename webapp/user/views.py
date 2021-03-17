from flask import (Blueprint, current_app, flash, redirect, render_template,
                   url_for)
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash

from webapp.model import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User

blueprint = Blueprint('user', __name__, template_folder='templates', url_prefix='/user')


@blueprint.route('/')
def user_main():
    title = 'Pricer'
    users = User.query.all()
    if users:
        print(f'user counter: {len(users)}')
    else:
        print('we lost user')
    return render_template('index.html', page_title=title,
                           users=users, menu=current_app.menu)


@blueprint.route('/login')
def login():
    print(f'url for login: {url_for("user.login")}')
    if current_user.is_authenticated:
        flash('You are logged in', 'success')
        return redirect(url_for('user.profile'))
    title = 'Login'
    login_form = LoginForm()
    return render_template('login.html', title=title,
                           menu=current_app.menu, form=login_form)


@blueprint.route('/profile')
@login_required
def profile():
    title = 'Profile'
    user = User.query.filter(User.id == current_user.get_id()).first()
    print(user)
    return render_template('profile.html', title=title,
                           menu=current_app.menu, user=user)


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


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        flash('You are already in da club, bro!', 'success')
        return redirect(url_for('user.profile'))

    title = 'Sign In'
    reg_form = RegistrationForm()
    menu = current_app.menu
    return render_template('register.html', title=title, menu=menu,
                           reg_form=reg_form)


@blueprint.route('/process-sign-in', methods=['POST'])
def process_sign_in():
    form = RegistrationForm()
    try:
        email = form.email.data
        password = generate_password_hash(form.password.data)
        firstname = form.firstname.data
        lastname = form.lastname.data
        city = form.city.data
        user = User(email=email, password=password, firstname=firstname,
                    lastname=lastname, city=city, role='user')
        # print(user)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('user registered successfully', 'success')
        return redirect('profile')
    except Exception as exp:
        print(f'Ошибка записи в БД: {exp}: {exp.args}')
        db.session.rollback()
        flash('Ошибка регистрации!', 'error')
        return redirect(url_for('register'))

