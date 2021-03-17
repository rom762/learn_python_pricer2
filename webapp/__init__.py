import os

from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required

from webapp.admin.admin import admin
from webapp.model import GPU, db
from webapp.news.views import blueprint as news_blueprint
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint
from webapp.weather import weather_city


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_pyfile("settings.py")
    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(news_blueprint)
    app.register_blueprint(admin)

    @login_manager.user_loader
    def load_user(user_id):
        print(f'load user {user_id}')
        return User.query.get(user_id)

    app.menu = {
        'Home': '/',
        'GPU': '/gpu',
        'News': '/news',
        'Weather': '/weather',
        'Register': '/user/register',
        'Login': '/user/login',
        'Profile': '/user/profile',
    }

    @app.route('/')
    @app.route('/index')
    def index():
        title = 'Pricer'
        users = User.query.all()
        if users:
            print(f'user counter: {len(users)}')
        else:
            print('we lost user')
        return render_template('index.html', page_title=title,
                               users=users, menu=app.menu)

    @app.route('/weather')
    def weather(city='Barcelona, Spain'):
        title = f'Weather in {city}'
        weather = weather_city(city_name=city)['data']
        current_city = weather['request'][0]['query']
        current_weather = weather['current_condition'][0]
        months = weather['ClimateAverages'][0]['month']

        return render_template(
            'weather.html', page_title=title,
            current_city=current_city, current_weather=current_weather,
            months=months, menu=app.menu)

    @app.route('/gpu')
    @login_required
    def gpu():
        gpus = GPU.query.all()
        return render_template(
            'gpu.html', menu=app.menu, title='Видеокарты', gpus=gpus)

    return app
