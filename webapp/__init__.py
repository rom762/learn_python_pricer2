import os
import logging

from flask import Flask, render_template
from flask_login import LoginManager, current_user, login_required

from webapp.model import db
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint

from webapp.gpu.models import GPU
from webapp.gpu.views import blueprint as gpu_blueprint


def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    app.config.from_pyfile("settings.py")
    logging.basicConfig(filename='webapp.log', level=logging.DEBUG)

    db.init_app(app)
    login_manager = LoginManager(app)
    login_manager.init_app(app)
    login_manager.login_view = 'user.login'
    app.register_blueprint(user_blueprint)
    app.register_blueprint(gpu_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        print(f'load user {user_id}')
        return User.query.get(user_id)

    app.menu = {
        'Home': '/',
        'GPU': '/gpu',
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

    return app
