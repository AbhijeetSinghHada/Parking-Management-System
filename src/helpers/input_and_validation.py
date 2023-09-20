import re
import maskpass

EMAIL_REGEX = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
USERNAME_REGEX = r"^[A-Za-z0-9]+(?:[ _-][A-Za-z0-9]+)*$"
PASSWORD_REGEX = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{5,}$"
VEHICLE_NUMBER_REGEX = r"^[A-Z]{2}\d{2}[A-Z]{2}\d{4}$"


def get_username_input():
    user_input = input("Enter Username : ")
    while not re.match(USERNAME_REGEX, user_input):
        print("Please Enter Username containing Alphabets, _ and numbers only : ")
        user_input = input("Enter Username : ")
    return user_input.strip()


def get_customer_id(message):
    user_input = input(message)
    if user_input == '':
        return user_input
    while not re.match(r'^[0-9]+$', user_input):
        print("Please Enter Valid Customer ID.")
        user_input = input(message)
    return user_input


def get_vehicle_number():
    user_input = input("Enter Vehicle Number : ")
    while not re.match(VEHICLE_NUMBER_REGEX, user_input):
        print("Please Enter Valid Vehicle Number. eg. (AB12CD3456)")
        user_input = input("Enter Vehicle Number : ")

    return user_input.strip()


def get_int_input(message):
    user_input = input(message).strip()
    while not re.match(r'^[0-9]+$', user_input):
        print("Invalid Input, Please try again.")
        user_input = input(message)
    return int(user_input)


def get_string_input(message):
    user_input = input(message)
    while not re.match(r'^[A-Za-z]+$', user_input):
        print("Invalid Input. Please try again.")
        user_input = input(message)
    return user_input


def input_validate_password():
    user_password = maskpass.askpass(prompt="Enter your password : ", mask="*")
    while not re.match(PASSWORD_REGEX, user_password):
        print("This is not a valid password.")
        user_password = maskpass.askpass(
            prompt="Enter your password : ", mask="*")
    return user_password


def input_validate_phone_number(message):
    user_input = input(message).strip()
    while not re.match(r'^\d{10}$', user_input):
        print("Invalid Phone Number, Please try again.")
        user_input = input(message)
    return int(user_input)


def input_validate_email(message):
    email = input(message)
    while not re.fullmatch(EMAIL_REGEX, email):
        print("Please enter a valid email address.")
        email = input(message)
    return email
