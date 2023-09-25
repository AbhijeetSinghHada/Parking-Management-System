from src.helpers import helpers

prompts = helpers.get_prompts()


class Customer:
    def __init__(self):
        self.name = None
        self.email_address = None
        self.phone_number = None
        self.customer_id = ''

