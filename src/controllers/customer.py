from src.helpers import input_and_validation


class Customer:
    def __init__(self):
        self.name = None
        self.email_address = None
        self.phone_number = None
        self.customer_id = ''

    def get_customer_details(self):
        self.customer_id = input_and_validation.get_customer_id(
            "Enter Customer ID (Leave if not known): ")
        self.name = input_and_validation.get_string_input("Enter Name : ")
        self.email_address = input_and_validation.input_validate_email(
            "Enter Email Address : ")
        self.phone_number = input_and_validation.input_validate_phone_number(
            "Enter Phone Number : ")

    def print_customer_details(self,customer_data):
        print("Customer ID : ", customer_data[0][0])
        print("Name : ", customer_data[0][1])
        print("Email Address : ", customer_data[0][2])
        print("Phone Number : ", customer_data[0][3])
