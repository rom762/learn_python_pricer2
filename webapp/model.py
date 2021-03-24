from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Regard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regard_id = db.Column(db.Integer, nullable=False)
    brand_name = db.Column(db.String)
    name = db.Column(db.String)
    picture = db.Column(db.String)
    price = db.Column(db.Float)

    def __repr__(self):
        return f'<regard: id:{self.id}\n, name: {self.name}\n, brand: {self.brand}\n, name: {self.name}>'


class Shop(db.Model):
    __tablename__ = 'shops'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    ulr = db.Column(db.String)

    def __repr__(self):
        return {'id': self.id, 'name': self.name, 'url': self.url}


class GpuPrice(db.Model):
    __tablename__ = 'gpu-prices'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Numeric, nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    created_on = db.Column(db.Date(), default=datetime.utcnow())


class GpuLink(db.Model):
    __tablename__ = 'gpu_links'
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'))
    link = db.Column(db.String)
    gpu_id = db.Column(db.Integer, db.ForeignKey('GPU.id'))
