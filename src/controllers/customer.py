from Parking_Management_System.src.helpers import validations
from src.helpers import helpers

prompts = helpers.get_prompts()


class Customer:
    def __init__(self):
        self.name = None
        self.email_address = None
        self.phone_number = None
        self.customer_id = ''

    def get_customer_details(self):
        print("Enter Customer Details : ")
        self.customer_id = validations.get_customer_id(
            prompts["prompts"]["INPUT_CUSTOMER_ID"])
        self.name = validations.get_string_input(
            prompts["prompts"]["INPUT_CUSTOMER_NAME"])
        self.email_address = validations.input_validate_email(
            prompts["prompts"]["INPUT_EMAIL"])
        self.phone_number = validations.input_validate_phone_number(
            prompts["prompts"]["INPUT_PHONE"])

        return self.customer_id, self.name, self.email_address, self.phone_number

    def print_customer_details(self, customer_data):
        print("\nCustomer Details : \n")
        print("Customer ID : ", customer_data[0][0])
        print("Name : ", customer_data[0][1])
        print("Email Address : ", customer_data[0][2])
        print("Phone Number : ", customer_data[0][3])
