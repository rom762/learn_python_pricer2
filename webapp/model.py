from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()

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
