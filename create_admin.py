from getpass import getpass
import sys

from webapp import create_app
from webapp.model import User, db

app = create_app()

with app.app_context():
    email = input('Введите email: ')

    if User.query.filter(User.email == email).count():
        print('Такой пользователь уже есть')
        sys.exit(0)
    # print('input pass')
    password = getpass('input pass: ')
    # print('repeat pass')
    password2 = getpass('repeat pass: ')

    if not password == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    new_user = User(email=email, role='admin')
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()
    print(f'User with id {new_user.id} added')