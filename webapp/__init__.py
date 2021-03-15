import os
from pprint import pprint

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.user.forms import LoginForm, RegistrationForm
from webapp.model import GPU, db
from webapp.user.models import User
from webapp.python_org_news import get_python_news
from webapp.queries import get_user_by_email, get_user_by_id
from webapp.weather import weather_city
from webapp.user.views import blueprint as user_blueprint
from webapp.news.views import blueprint as news_blueprint
from webapp.admin.admin import admin



def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_pyfile("settings.py")
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    app.register_blueprint(user_blueprint, url_prefix='/user')
    app.register_blueprint(news_blueprint, url_prefix='/news')
    app.register_blueprint(admin, url_prefix='/admin')

    @login_manager.user_loader
    def load_user(user_id):
        print('load user')
        return User.query.get(user_id)

    menu = {
        'Home': '/',
        'GPU': '/gpu',
        'News': '/news',
        'Weather': '/weather',
        'Register': '/register',
        'Login': '/login',
        'Profile': '/profile',
    }

    @app.route('/')
    @app.route('/index')
    def index():
        title = 'Pricer'
        users = User.query.all()
        if users:
            print(f'user counter: {len(users)}')
        else:
            print('we lost users')
        return render_template('index.html', page_title=title, users=users, menu=menu)

    @app.route('/weather')
    def weather(city='Barcelona, Spain'):
        title = f'Weather in {city}'
        weather = weather_city(city_name=city)['data']
        current_city = weather['request'][0]['query']
        current_weather = weather['current_condition'][0]
        months = weather['ClimateAverages'][0]['month']

        return render_template('weather.html', page_title=title, current_city=current_city,
                               current_weather=current_weather,
                               months=months, menu=menu)

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            flash('You are already in da club, bro!', 'success')
            return redirect(url_for('profile'))

        title = 'Sign In'
        reg_form = RegistrationForm()
        return render_template('register.html', title=title, menu=menu, reg_form=reg_form)

    @app.route('/process-sign-in', methods=['POST'])
    def process_sign_in():
        form = RegistrationForm()
        try:
            email = form.email.data
            password = generate_password_hash(form.password.data)
            firstname = form.firstname.data
            lastname = form.lastname.data
            city = form.city.data
            user = User(email=email, password=password, firstname=firstname, lastname=lastname, city=city,
                        role='user')
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
            return redirect('register')

    @app.route('/profile')
    @login_required
    def profile():
        user = User.query.filter(User.id == current_user.get_id()).first()
        return render_template('profile.html', menu=menu, title='Profile', user=user)

    @app.route('/gpu')
    @login_required
    def gpu():
        gpus = GPU.query.all()
        return render_template('gpu.html', menu=menu, title='Видеокарты', gpus=gpus)


    return app
