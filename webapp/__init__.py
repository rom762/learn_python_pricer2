from flask import Flask, render_template


def create_app():
    app = Flask(__name__)
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
        return render_template('index.html', page_title=title, menu=menu)

    return app
