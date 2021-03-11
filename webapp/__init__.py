import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, flash, redirect, url_for
from webapp.weather import weather_city
from webapp.python_org_news import get_python_news
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, login_user, login_required
from webapp.model import db, Users, Profiles, News, GPU
from webapp.UserLogin import UserLogin
from webapp.queries import get_user_by_email

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_pyfile("settings.py")
    db.init_app(app)

    login_manager = LoginManager(app)

    @login_manager.user_loader
    def load_user(user_id):
        print('load user')
        return UserLogin().fromDB(user_id, db)



    menu = {
        'Home': '/',
        'News': '/news',
        'Weather': '/weather',
        'Register': '/register',
        'GPU': '/gpu',
        'Авторизация': '/login',
    }

    @app.route('/')
    @app.route('/index')
    def index():
        title = 'Pricer'
        users = Users.query.all()
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
                hash = generate_password_hash(request.form['psw'])
                u = Users(email=request.form['email'], psw=hash)
                db.session.add(u)
                db.session.flush()  # пока в памяти

                p = Profiles(firstname=request.form['firstname'], lastname=request.form['lastname'],
                             city=request.form['city'], user_id=u.id)
                db.session.add(p)
                db.session.commit()  # а вот тут уже пишем в базу

                print('user added to the base')
                flash('User registered successfully', 'success')
                return redirect(url_for('index'))

            except Exception as exp:
                db.session.rollback()  # откатываем изменения
                print(f"Ошибка добавления в БД: {exp}")
                flash('something goes wrong!', 'error')
        return render_template('register.html', title='Registration', menu=menu)

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        if request.method == 'POST':
            user = get_user_by_email(request.form['email'])
            password = check_password_hash(user.psw, request.form['psw'])
            if user and password:
                user_login = UserLogin().create(user)

                login_user(user_login)
                return redirect(url_for('gpu'))
            flash("Email or password is wrong.")

        return render_template('login.html', menu=menu, title='Авторизация')

    @app.route('/gpu')
    @login_required
    def gpu():
        gpus = GPU.query.all()
        return render_template('gpu.html', menu=menu, title='Видеокарты', gpus=gpus)

    return app
