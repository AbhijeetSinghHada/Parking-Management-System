from src.controllers.customer import Customer
from src.helpers import helpers
import logging
logger = logging.getLogger(__name__)


class Vehicle(Customer):
    def __init__(self, db_helpers):
        self.sql_queries = helpers.get_sql_queries()
        super().__init__()
        self.vehicle_number = None
        self.vehicle_type = None
        self.db_helpers = db_helpers

    def print_vehicle_details(self, data):
        logger.debug("print_vehicle_details called with params {}".format(data))
        print("Vehicle Details : ")
        for i in data:
            print(f'Customer ID : {i[0]}')
            print(f'Customer Name : {i[1]}')
            print(f'Customer Email Address : {i[2]}')
            print(f'Customer Phone Number : {i[3]}')
            print(f'Vehicle Number : {i[4]}')
            print(f'Vehicle Type : {i[5]}')


    def check_if_vehicle_exists(self, vehicle_number):
        logger.debug("check_if_vehicle_exists called with params {}".format(vehicle_number))
        data = self.db_helpers.get_vehicle_data(vehicle_number=vehicle_number)
        if data:
            self.set_vehicle_customer_data(data)
            return data
        return None


    def add_vehicle(self, vehicle_number, vehicle_type):
        logger.debug("add_vehicle called with params {},{}".format(vehicle_number,vehicle_type))

        self.db_helpers.insert_vehicle(vehicle_number, vehicle_type)
        print("\nVehicle Added Successfully.\n")

    def add_vehicle_category(self, slot_type, total_capacity, parking_charge):

        self.db_helpers.add_vehicle_category(slot_type, total_capacity, parking_charge)
        print("\nVehicle Category Added Successfully.\n")

    def set_vehicle_customer_data(self, data):
        logger.debug("set_vehicle_customer_data called with params {}".format(data))
        self.customer_id = data[0][0]
        self.name = data[0][1]
        self.email_address = data[0][2]
        self.phone_number = data[0][3]
        self.vehicle_number = data[0][4]
        self.vehicle_type = data[0][5]
