from flask_sqlalchemy import SQLAlchemy

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


class Regard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regard_id = db.Column(db.Integer, nullable=False)
    brand_name = db.Column(db.String)
    name = db.Column(db.String)
    picture = db.Column(db.String)
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<regard: id:{self.id}\n, name: {self.name}\n, brand: {self.brand}\n, name: {self.name}>'
