import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, render_template, request, flash, redirect, url_for
from webapp.weather import weather_city
from webapp.python_org_news import get_python_news
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from webapp.model import db, Users, Profiles, News


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_pyfile("settings.py")
    db.init_app(app)

    menu = {
        'Home': '/',
        'News': '/news',
        'Weather': '/weather',
        'Register': '/register',
        # 'Авторизация': '/login',
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
        weather = weather_city(city_name=city)
        current_city = weather['data']['request'][0]['query']
        current_weather = weather['data']['current_condition'][0]
        months = weather['data']['ClimateAverages'][0]['month']
        # pprint(weather)
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

    @app.route('/login')
    def login():
        return render_template('login.html', menu=menu, title='Авторизация')

    return app
#
# if __name__ == "__main__":
#     app.secret_key = os.urandom(24)
#     app.run(debug=True)
