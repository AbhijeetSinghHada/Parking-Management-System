from src.controllers.login import Login
from controllers.menu import Menu
from src.models.database import Database


def login_menu():
    user_input = None
    while user_input != '2':
        print("Hello Welcome to Park+!! Choose from the options below - ")
        print("1) Login")
        print("2) Exit")

        user_input = input("Your Choice - ")
        if user_input == '1':
            try:
                db = Database()
                login = Login(db)
                login.authenticate()
                user_data = login.fetch_user_roles()
                Menu(user_data, db)

            except Exception as e:
                print(e)


if __name__ == "__main__":
    login_menu()
