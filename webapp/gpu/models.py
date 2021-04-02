from webapp.model import db
from datetime import datetime
from sqlalchemy.orm import relationship


class GPU(db.Model):
    __tablename__ = 'GPU'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    vendor = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    picture = db.Column(db.String, nullable=True)
    model = db.Column(db.String, nullable=False, unique=True)

    def __repr__(self):
        elem = {
            'id': self.id,
            'vendor': self.vendor,
            'name': self.name,
            'picture': self.picture,
            'model': self.model,
        }
        return elem


class Citilink(db.Model):
    __tablename__ = 'citilink'
    id = db.Column(db.Integer, primary_key=True)
    citilink_id = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    old_price = db.Column(db.Float, nullable=False)
    short_name = db.Column(db.String, nullable=False)
    category_name = db.Column(db.String, nullable=False)
    brand_name = db.Column(db.String, nullable=False)
    club_price = db.Column(db.String, nullable=True)
    picture = db.Column(db.String, nullable=False)
    url = db.Column(db.String)
    model = db.Column(db.String)

    def __repr__(self):
        return f'<citilink_gpu: id:{self.id}\n, ' \
               f'shortname: {self.shortName}\n, ' \
               f'price: {self.price}>'


class Regard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    regard_id = db.Column(db.Integer, nullable=False)
    brand = db.Column(db.String)
    name = db.Column(db.String)
    picture = db.Column(db.String)
    price = db.Column(db.Numeric)
    url = db.Column(db.String)
    model = db.Column(db.String)

    def __repr__(self):
        return f'<regard: id:{self.id}\n, name: {self.name}\n, brand: {self.brand}\n, name: {self.name}>'


class GpuPrice(db.Model):
    __tablename__ = 'gpu_prices'
    id = db.Column(db.Integer, primary_key=True)
    gpu_id = db.Column(db.Integer, db.ForeignKey('GPU.id'), index=True, nullable=False)
    price = db.Column(db.Numeric, nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'), index=True, nullable=False)
    created_on = db.Column(db.DateTime(), default=datetime.utcnow(), nullable=False)



class GpuLink(db.Model):
    __tablename__ = 'gpu_links'
    id = db.Column(db.Integer, primary_key=True)
    shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
    gpu_id = db.Column(db.Integer, db.ForeignKey('GPU.id'))
    shop_gpu_id = db.Column(db.String, nullable=False, unique=True)
    url = db.Column(db.String)

#
#
# class GpuInShops(db.Model):
#     __tablename__ = 'gpu_in_shops'
#     id = db.Column(db.Integer, primary_key=True)
#     gpu_id = db.Column(db.Integer, db.ForeignKey('GPU.id'))
#     shop_id = db.Column(db.Integer, db.ForeignKey('shop.id'))
#     link = db.Column(db.String)
#     created_on = db.Column(db.Date(), default=datetime.utcnow())
