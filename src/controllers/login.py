from src.utils.sql_queries import fetch_user_details
import hashlib
from src.helpers.errors import AuthenticationError
from src.utils import sql_queries
from src.helpers import input_and_validation
from src.helpers.helpers import convert_user_details_to_dict


class Login:
    def __init__(self, db):
        self.username = None
        self.password = None
        self.user_id = None
        self.user_data = None
        self.db = db
        self.__get_user_credentials()

    def __get_user_credentials(self):
        self.username = input_and_validation.get_username_input()
        password = input_and_validation.input_validate_password()
        self.password = self.get_hashed_password(password)

    def fetch_user_roles(self):
        self.user_data = self.db.get_multiple_items(
            fetch_user_details, (self.user_id,))
        self.user_data = convert_user_details_to_dict(self.user_data)
        return self.user_data

    def authenticate(self):
        data = self.db.get_multiple_items(
            sql_queries.fetch_login_details, (self.username, self.password))
        if data:
            self.user_id = data[0][0]
            return self.user_id
        raise AuthenticationError('Invalid Login Details')

    @staticmethod
    def get_hashed_password(password):
        password = password.encode()
        return hashlib.sha256(password).hexdigest()


if __name__ == '__main__':
    ls = Login.get_hashed_password('1234Kittu')
    print(ls)
