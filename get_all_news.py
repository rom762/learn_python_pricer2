from webapp import create_app, get_python_news

app = create_app()
with app.app_context():
    get_python_news()