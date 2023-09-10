"""Main module to run the application"""
import logging
import traceback

from src.controllers.login import Login
from src.controllers.menu import Menu
from src.helpers.helpers import get_prompts
from src.models.database import Database
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    filename='logs.txt')

logger = logging.getLogger(__name__)
prompts = get_prompts()


def login_menu():
    """login_menu function is used to display the login menu and authenticate the user"""
    user_input = None
    while user_input != '2':
        print(prompts["menu"]["LOGIN_VIEW"])

        user_input = input("Your Choice - ")
        if user_input == '1':
            try:
                db = Database()
                login = Login(db)
                login.authenticate()
                user_data = login.fetch_user_roles()
                Menu(user_data, db)

            except Exception as e:
                logger.debug(traceback.print_exc())
                print(e)


if __name__ == "__main__":
    login_menu()
