import enum

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

    def __str__(self):
        return f'<users {self.id, self.email, self.pr.firstname, self.pr.lastname, self.psw}>'

    def __repr__(self):
        return {'id': self.id, 'email': self.email, 'psw' : self.psw}


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
    category_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    old_price = db.Column(db.Float, nullable=False)
    short_name = db.Column(db.String, nullable=False)
    category_name = db.Column(db.String, nullable=False)
    brand_name = db.Column(db.String, nullable=False)
    club_price = db.Column(db.String, nullable=True)
    picture = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<GPU: id:{self.id}\n, shortname: {self.shortName}\n, price: {self.price}>'