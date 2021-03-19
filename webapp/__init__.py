import os

from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (LoginManager, current_user, login_required,
                         login_user, logout_user)
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.forms import LoginForm
from webapp.model import GPU, News, User, db
from webapp.python_org_news import get_python_news
from webapp.queries import get_user_by_email, get_user_by_id
from webapp.weather import weather_city


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_pyfile("settings.py")
    db.init_app(app)

    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        print('load user')
        return User.query.get(user_id)

    menu = {
        'Home': '/',
        'GPU': '/gpu',
        # 'News': '/news',
        # 'Weather': '/weather',
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
            print(len(users))
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

    @app.route('/news')
    def news():
        title = 'Python News'
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('news.html', page_title=title, news_list=news_list, menu=menu)

    @app.route('/register', methods=('POST', 'GET'))
    def register():
        if request.method == 'POST':

            # TODO добавить проверку на корректность введенных данных

            try:
                password_hash = generate_password_hash(request.form['password'])
                user = User(email=request.form['email'],
                            password=password_hash,
                            firstname=request.form['firstname'],
                            lastname=request.form['lastname'],
                            city=request.form['city'],
                            role='user')

                db.session.add(user)
                db.session.commit()
                print(f'User {user.firstname} {user.lastname} registered successfully')
                flash('User registered successfully', 'success')
                return redirect(url_for('index'))

            except Exception as exp:
                db.session.rollback()  # откатываем изменения
                print(f"Ошибка добавления в БД: {exp}")
                flash('something goes wrong!', 'error')
        return render_template('register.html', title='Registration', menu=menu)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            flash('You are logged in', 'success')
            return redirect(url_for('index'))
        title = 'Login'
        login_form = LoginForm()
        return render_template('login.html', title=title, menu=menu, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        login_form = LoginForm()
        if login_form.validate_on_submit():
            user = User.query.filter_by(email=login_form.email.data).first()
            if user and user.check_password(login_form.password.data):
                login_user(user, remember=login_form.remember_me.data)
                flash('You are logged in', 'success')
                return redirect(url_for('gpu'))
        flash('Неправильное имя пользователя или пароль', 'warning')
        return redirect(url_for('login'))

    @app.route('/logout')
    @login_required
    def logout():
        flash('You are logged out.', 'primary')
        logout_user()
        return redirect(url_for('login'))

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

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'Привет админ'
        else:
            return 'Ты не админ!'

    return app
