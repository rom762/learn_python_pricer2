from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from webapp.model import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(500), nullable=True)  # не пустое, под хеш пароля
    role = db.Column(db.String(10), index=True)
    firstname = db.Column(db.String(50))
    lastname = db.Column(db.String(50))
    city = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def is_admin(self):
        return self.role == 'admin' or self.role == 'root'

    def __str__(self):
        return f'<users {self.id, self.email, self.firstname, self.lastname, self.password}>'

    def __repr__(self):
        return {'id': self.id, 'email': self.email, 'password' : self.password, 'role': self.role}
