from webapp.model import Users


def get_user_by_id(user_id):
    try:
        user = Users.query.filter(Users.id == user_id).first()
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
        user = Users.query.filter(Users.email == email).first()

        if not user:
            print(f'user with email: {email} not found!')
            return None
        return user

    except Exception as exp:
        print(f'Get data from Database error: {exp}')

    return None


if __name__ == '__main__':
    from webapp import create_app
    app = create_app()
    with app.app_context():
        user = get_user_by_email('jack@yahoo.com')
        print(user.psw)



