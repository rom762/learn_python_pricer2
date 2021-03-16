from webapp.model import db


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)


if __name__ == "__main__":
    # не работает
    from webapp import create_app
    app = create_app()
    db.init_app(app)
    with app.app_context():
        news = News.query.all()
        print(news)