from webapp import create_app

from webapp.model import db
from webapp.user.models import User
from webapp.gpu.models import GPU

from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def get_user_by_id(user_id):
    try:
        user = User.query.filter(User.id == user_id).first()
        if not user:
            print('user not found!')
            return None
        return user
    except Exception as exp:
        print(f'Get data from Database error: {exp}')

    return None


def get_user_by_email(email):
    print(f'email: {email}')
    try:
        user = User.query.filter(User.email == email).first()
        if not user:
            print(f'user with email: {email} not found!')
            return None
        return user

    except Exception as exp:
        print(f'Get data from Database error: {exp}')

    return None


def find_equals_gpu(gpu, list_to_find):
    pass


def get_gpu():
    return GPU.query.all()



if __name__ == '__main__':
    # from webapp import create_app
    # app = create_app()
    # with app.app_context():
    #     user = get_user_by_email('jack@yahoo.com')
    #     print(user.psw)

    # a = fuzz.ratio('Привет мир', 'Привет мир')
    # print(a)
    # get_gpu()

    app = create_app()
    with app.app_context():
        gpus = get_gpu()
        for gpu in gpus:
            print(gpu.id, gpu.model)





