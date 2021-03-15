from webapp.queries import get_user_by_id
from webapp.model import User, db


class UserLogin:

    def create(self, user):
        self.__user = user
        print(user)
        return self

    def from_db(self, user_id, db):
        self.__user = User.get_user_by_id(user_id)
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return True

    def get_id(self):
        return str(self.__user.id)