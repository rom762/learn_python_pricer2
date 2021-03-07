from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, unique=True, nullable=False)
    published = db.Column(db.DateTime, nullable=False)
    text = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    psw = db.Column(db.String(500), nullable=True)  # не пустое, под хеш пароля
    date = db.Column(db.DateTime, default=datetime.utcnow)

    pr = db.relationship('Profiles', backref='users', uselist=False)

    def __repr__(self):
        return f'<users {self.id}>'

    def getUser(self):
        return self


class Profiles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=True)
    lastname = db.Column(db.String(50), nullable=True)
    city = db.Column(db.String(100))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<profiles {self.id}>'


class GPU(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    citilink_id = db.Column(db.Integer, nullable=False)
    categoryId = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    oldPrice = db.Column(db.Float, nullable=False)
    shortName = db.Column(db.String, nullable=False)
    categoryName = db.Column(db.String, nullable=False)
    brandName = db.Column(db.String, nullable=False)
    clubPrice = db.Column(db.String, nullable=True)
    picture = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<GPU: id:{self.id}\n, shortname: {self.shortName}\n, price: {self.price}>'
