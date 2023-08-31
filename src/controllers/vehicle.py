from tabulate import tabulate
from src.controllers.customer import Customer
from src.helpers import errors, input_and_validation, helpers


class Vehicle(Customer):
    def __init__(self, db):
        self.sql_queries = helpers.get_sql_queries()
        super().__init__()
        self.vehicle_number = None
        self.vehicle_type = None
        self.db = db

    def get_vehicle_data(self, vehicle_number='', customer_id='', email_address=''):
        vehicles = self.db.get_multiple_items(self.sql_queries["fetch_vehicle_data"],
                                              (vehicle_number, customer_id, email_address))
        return vehicles

    def print_vehicle_details(self, data):
        print("Vehicle Details : ")
        for index, i in enumerate(data):
            print(f'Customer ID : {i[0]}')
            print(f'Customer Name : {i[1]}')
            print(f'Customer Email Address : {i[2]}')
            print(f'Customer Phone Number : {i[3]}')
            print(f'Vehicle Number : {i[4]}')
            print(f'Vehicle Type : {i[5]}')

    def set_vehicle_customer_data(self, data):
        self.customer_id = data[0][0]
        self.name = data[0][1]
        self.email_address = data[0][2]
        self.phone_number = data[0][3]
        self.vehicle_number = data[0][4]
        self.vehicle_type = data[0][5]

    def check_if_vehicle_exists(self, vehicle_number):
        data = self.get_vehicle_data(vehicle_number=vehicle_number)
        if data:
            self.set_vehicle_customer_data(data)
            return data
        return None

    def fetch_slot_types(self):
        slot_types = self.db.get_multiple_items(
            self.sql_queries["fetch_slot_types"])
        slot_types_modified_list = [x[0] for x in slot_types]
        print("Vehicle Categories are : ")
        index_slot_types = enumerate(slot_types_modified_list, start=1)
        print(tabulate(index_slot_types, headers=[
              'Index', 'Vehicle Category']))
        return slot_types

    def add_vehicle(self):
        self.vehicle_number = input_and_validation.get_vehicle_number()
        data = self.check_if_vehicle_exists(self.vehicle_number)
        if data:
            print("\nVehicle Already Exists.\n")
            self.print_vehicle_details(data)
            return
        slot_types = self.fetch_slot_types()
        user_inp = int(input('Select Vehicle Type : '))
        while user_inp > len(slot_types) or user_inp < 1:
            user_inp = int(
                input(f'Please Enter Vehicle Type index between {1} - {len(slot_types)}: '))
        self.vehicle_type = slot_types[user_inp-1][0]
        print("Enter Customer Details : ")
        self.get_customer_details()
        customer_data = self.db.get_multiple_items(
            self.sql_queries["fetch_customer_data"], (self.customer_id, self.email_address, self.phone_number))
        if customer_data:
            self.db.update_item(
                self.sql_queries["insert_vehicle_by_customer_id"],
                (customer_data[0][0], self.vehicle_number, self.vehicle_type))
            return
        self.db.update_item(
            self.sql_queries["insert_customer"], (self.name, self.email_address, self.phone_number))
        self.db.update_item(
            self.sql_queries["insert_vehicle"], (self.vehicle_number, self.vehicle_type))

        print("\nVehicle Added Successfully.\n")

    def add_vehicle_category(self):
        existing_vehicles = self.fetch_existing_types()
        slot_type = input_and_validation.get_string_input(
            "Enter Slot Type Name : ")
        for i in existing_vehicles:
            if slot_type.lower() == i[1].lower():
                raise errors.DuplicateEntry("Slot Type Already Exists.")
        total_capacity = input_and_validation.get_int_input(
            "Total Capacity : ")
        while total_capacity == '':
            total_capacity = input_and_validation.get_int_input(
                "Total Capacity : ")
        self.db.update_item(
            self.sql_queries["add_vehicle_type"], (slot_type, total_capacity))
        parking_charge = input_and_validation.get_int_input(
            "Enter the Charge Per Hour : ")
        self.db.update_item(
            self.sql_queries["add_to_charges_tables"], (parking_charge,))
        print("\nVehicle Category Added Successfully.\n")

    def fetch_existing_types(self):
        vehicle_types = self.db.get_multiple_items(
            self.sql_queries["fetch_vehicle_types"])
        return vehicle_types
