import traceback

from tabulate import tabulate

from src.controllers.billing import Billing
from src.controllers.parking_space import ParkingSpace
from src.helpers import input_and_validation, errors
from src.helpers.helpers import get_prompts, check_input_in_range, return_date_and_time
from src.models.database import Database
from src.models.database_helpers import DatabaseHelper
from src.utils.access_decorator import access_identifier
from src.controllers.slot import Slot
from src.controllers.vehicle import Vehicle
from src.configurations import config
from src.helpers.input_and_validation import get_vehicle_number
import logging

logger = logging.getLogger(__name__)
prompts = get_prompts()


class Menu:
    user_details = {}

    def __init__(self, user_details_dict, db):
        self.db_helper = DatabaseHelper(db)
        self.user_details_dict = user_details_dict
        self.action_role_mapping = config.action_role_mapping
        self.menu()

    @access_identifier
    def assign_slot(self):
        """This Function is used to assign slot to a vehicle.
        It takes vehicle number as input and checks if the vehicle exists in the database.
        If it does not exist, it asks the user if they want to add the vehicle.
        If the vehicle exists, it checks if the vehicle type matches the slot type.
        If it does not match, it asks the user to try again.
        If it matches, it assigns the slot to the vehicle."""

        print("Functionality : Assign Slot\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        slot = Slot(self.db_helper)
        parking_space = ParkingSpace(self.db_helper)
        attributes = parking_space.get_parking_slot_attributes()
        selected_vehicle_type = attributes[0]
        slot.display_slot_table_by_category(selected_vehicle_type)

        slot_number = check_input_in_range(
            "Enter Slot Number : ", attributes[1])
        slot.check_if_slot_already_occupied(slot_number, selected_vehicle_type)

        vehicle_number = get_vehicle_number()
        slots_data = self.db_helper.get_slots_data()

        for i in slots_data:
            if i[5] == vehicle_number:
                print("Vehicle Already has a slot assigned.")
                return

        data = slot.check_if_vehicle_exists(vehicle_number)
        if not data:
            print("Vehicle Does not Exist!")
            self.add_vehicle()
            return

        fetched_vehicle_type = data[0][5]
        if selected_vehicle_type != fetched_vehicle_type:
            print("Wrong slot type for vehicle! Try Again.")
            return

        slot.set_vehicle_customer_data(data)
        date, time = return_date_and_time()
        billing = Billing(self.db_helper)
        billing.insert_into_bill_table(vehicle_number, date, time)
        slot.assign_slot(slot_number, vehicle_number, selected_vehicle_type)

    @access_identifier
    def add_vehicle(self):
        """This Function is used to add a vehicle to the database.
        It takes vehicle number as input and checks if the vehicle exists in the database. If it do not exist,
        it asks for vehicle details and adds the vehicle to the database.
        if it exists, it prints the vehicle details."""

        print("Functionality : Add Vehicle\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        vehicle = Vehicle(self.db_helper)
        vehicle_number = input_and_validation.get_vehicle_number()
        data = vehicle.check_if_vehicle_exists(vehicle_number)
        if data:
            print("\nVehicle Already Exists.\n")
            vehicle.print_vehicle_details(data)
            return
        parking_space = ParkingSpace(self.db_helper)
        attributes = parking_space.get_parking_slot_attributes()
        selected_vehicle_type = attributes[0]
        customer_details = vehicle.get_customer_details()
        customer_data = self.db_helper.fetch_customer_data(
            vehicle.customer_id, vehicle.email_address, vehicle.phone_number)
        if customer_data:
            customer_id = customer_data[0][0]
            self.db_helper.insert_vehicle_by_customer_id(
                customer_id, vehicle_number, selected_vehicle_type)
            vehicle.print_customer_details(customer_data)
            return
        customer_details = customer_details[1:]
        self.db_helper.insert_customer_details(*customer_details)
        vehicle.add_vehicle(vehicle_number, selected_vehicle_type)

    @access_identifier
    def driver_add_vehicle_category(self):
        """This Function is used to add a vehicle category to the database.
        It takes vehicle category, capacity and charge per hour as input and adds it to the database."""
        print("Functionality : Add Vehicle Category\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        logger.debug("add_vehicle_category called")

        vehicle = Vehicle(self.db_helper)
        print("Available Slots Types and Parking Capacity : \n")
        Menu.check_parking_capacity(self)
        existing_vehicles = self.db_helper.get_vehicle_category_data()
        slot_type = input_and_validation.get_string_input(
            "Enter Slot Type Name : ")
        for i in existing_vehicles:
            if slot_type.lower() == i[0].lower():
                raise errors.DuplicateEntry("Slot Type Already Exists.")
        total_capacity = input_and_validation.get_int_input(
            "Total Capacity : ")
        parking_charge = input_and_validation.get_int_input(
            "Enter the Charge Per Hour : ")
        vehicle.add_vehicle_category(slot_type, total_capacity, parking_charge)

    @access_identifier
    def check_parking_capacity(self):
        """This Function is used to Total parking capacity of the parking lot as well as,
         charges associated with each type of vehicle category"""
        print("Functionality : Check Parking Capacity\n")
        vehicle_types = self.db_helper.get_vehicle_category_data()
        print(tabulate(vehicle_types, headers=['Slot Type', 'Total Capacity', 'Charge'],
                       showindex=range(1, len(vehicle_types) + 1)))

    @access_identifier
    def driver_update_parking_space(self):
        """This Function is used to update the parking capacity of a vehicle category.
        It takes vehicle category and new capacity as input and updates the parking capacity."""
        print("Functionality : Update Parking Space\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        parking_space = ParkingSpace(self.db_helper)
        attributes = parking_space.get_parking_slot_attributes()
        new_capacity = input_and_validation.get_int_input(
            prompts["prompts"]["INPUT_NEW_CAPACITY"])
        parking_category = attributes[0]
        if new_capacity < int(attributes[1]) and parking_space.are_vehicles_already_parked(parking_category,
                                                                                           new_capacity):
            raise ValueError("First Remove Vehicles From Parking Space Range")
        parking_space.update_parking_capacity(new_capacity, parking_category)

    @access_identifier
    def unassign_slot(self):
        """This Function is used to unassign slot for a vehicle.
        It takes vehicle number as input and unassigns the slot."""
        print("Functionality : Unassign Slot\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return

        vehicle_number = get_vehicle_number()
        slots_data = self.db_helper.get_slots_data()
        for i in slots_data:
            if i[5] == vehicle_number:
                slot_id = i[7]
                slot_charges = i[6]
                billing = Billing(self.db_helper)
                bill_id = i[4]
                billing.update_bill_table(bill_id, slot_charges)
                bill = billing.generate_bill(bill_id)
                billing.print_bill(bill)
                slot = Slot(self.db_helper)
                slot.unassign_slot(slot_id)
                return
        print("Vehicle do not have any assigned slot.")

    @access_identifier
    def ban_slot(self):
        """This Function is used to ban a slot.
        It takes slot type and slot number as input and bans the slot."""
        print("Functionality : Ban Slot\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        slot = Slot(self.db_helper)
        parking_space = ParkingSpace(self.db_helper)
        attributes = parking_space.get_parking_slot_attributes()
        vehicle_type = attributes[0]
        slot.display_slot_table_by_category(vehicle_type)
        slot_number = check_input_in_range(
            "Enter Slot Number : ", attributes[1])
        slot.check_if_slot_already_occupied(slot_number, vehicle_type)
        slot.ban_slot(slot_number, vehicle_type)

    @access_identifier
    def driver_unban_slot(self):
        """This Function is used to unban a slot.
        It takes slot number as input and unbans the slot."""
        print("Functionality : Unban Slot\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        slot = Slot(self.db_helper)
        data = slot.view_ban_slots()
        slot_number_index = check_input_in_range(
            "Enter Slot Number Index to Unban : ", len(data))
        slot_number = data[slot_number_index - 1][0]
        slot_type = data[slot_number_index - 1][1]
        slot.unban_slot(slot_number, slot_type)

    @access_identifier
    def update_parking_charges(self):
        """This Function is used to update the parking charges of a vehicle category.
        It takes vehicle category and new charges as input and updates the parking charges."""
        print("Functionality : Update Parking Charges\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        parking_space = ParkingSpace(self.db_helper)

        parking_space.update_parking_charges()

    @access_identifier
    def view_ban_slots(self):
        """This Function is used to view all the banned slots."""
        print("Functionality : View Ban Slots\n")
        slot = Slot(self.db_helper)
        slot.view_ban_slots()

    def operator_choices(self, choice):
        if choice == 1:
            return Menu.check_parking_capacity
        if choice == 2:
            return Menu.add_vehicle
        if choice == 3:
            return Menu.assign_slot
        if choice == 4:
            return Menu.unassign_slot

    def admin_choices(self, choice):
        if choice == 1:
            return Menu.check_parking_capacity
        if choice == 2:
            return Menu.driver_add_vehicle_category
        if choice == 3:
            return Menu.driver_update_parking_space
        if choice == 4:
            return Menu.update_parking_charges 
        if choice == 5:
            return Menu.ban_slot
        if choice == 6:
            return Menu.driver_unban_slot
        if choice == 7:
            return Menu.view_ban_slots

    def admin_view(self, choice):
        if choice == 1:
            self.admin_menu()
            return
        if choice == 2:
            self.operator_menu()
            return

    def menu(self):
        if 1 in self.user_details_dict['roles']:
            self.menu_choice_admin()
        if 2 in self.user_details_dict['roles']:
            self.operator_menu()

    def menu_choice_admin(self):
        while True:
            print(prompts["menu"]["ADMIN_MENU_VIEW"])
            user_choice = input_and_validation.get_int_input('Your Choice - ')
            if user_choice == 3:
                return
            if user_choice > 3:
                print("Invalid Choice.")
                continue
            try:
                self.admin_view(user_choice)
            except Exception as e:
                logger.debug(e)
                print(e)

    def admin_menu(self):
        while True:
            print(prompts['menu']["ADMIN_VIEW"])
            user_choice = input_and_validation.get_int_input('Your Choice - ')
            if user_choice == 8:
                return
            if user_choice > 8:
                print("Invalid Choice.")
                continue
            try:
                self.admin_choices(user_choice)(self)
            except Exception as e:
                logger.debug(e)
                print(e)

    def operator_menu(self):
        while True:
            print(prompts["menu"]["OPERATOR_VIEW"])
            user_choice = input_and_validation.get_int_input('Your Choice - ')
            if user_choice == 5:
                return
            if user_choice > 5:
                print("Invalid Choice.")
                continue
            try:
                self.operator_choices(user_choice)(self)
            except Exception as e:
                logger.debug(e)
                print(e)


if __name__ == '__main__':
    test_db = Database()
    Menu({"name": "Kittu", "user_id": 2, "roles": [1, 2]}, test_db)
