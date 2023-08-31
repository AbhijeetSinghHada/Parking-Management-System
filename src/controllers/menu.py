import traceback

from tabulate import tabulate
from src.controllers.parking_space import ParkingSpace
from src.helpers import input_and_validation
from src.models.database import Database
from src.utils.access_decorator import access_identifier
from src.controllers.slot import Slot
from src.controllers.vehicle import Vehicle
from src.configurations import config
from src.helpers.input_and_validation import get_vehicle_number
from src.utils import prompts
import logging
logger = logging.getLogger(__name__)


class Menu:
    user_details = {}
    db = None

    def __init__(self, user_details_dict, db):
        self.db = db
        self.user_details_dict = user_details_dict
        self.action_role_mapping = config.action_role_mapping
        self.menu()

    @access_identifier
    def assign_slot(self):
        '''This Function is used to assign slot to a vehicle. 
        It takes vehicle number as input and checks if the vehicle exists in the database. 
        If it does not exist, it asks the user if they want to add the vehicle. 
        If the vehicle exists, it checks if the vehicle type matches the slot type. 
        If it does not match, it asks the user to try again. 
        If it matches, it assigns the slot to the vehicle.'''

        print("Functionality : Assign Slot\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        slot = Slot(self.db)
        slot.assign_slot()

    @access_identifier
    def add_vehicle(self):
        '''This Function is used to add a vehicle to the database. 
        It takes vehicle number as input and checks if the vehicle exists in the database. If it do not exist, 
        it asks for vehicle details and adds the vehicle to the database.
        if it exists, it prints the vehicle details.'''

        print("Functionality : Add Vehicle\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        vehicle = Vehicle(self.db)
        vehicle.add_vehicle()

    @access_identifier
    def add_vehicle_category(self):
        '''This Function is used to add a vehicle category to the database. 
        It takes vehicle category, capacity and charge per hour as input and adds it to the database.'''
        print("Functionality : Add Vehicle Category\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        vehicle = Vehicle(self.db)
        print("Available Slots and Parking Capacity : \n")
        Menu.check_parking_capacity(self)
        vehicle.add_vehicle_category()

    @access_identifier
    def check_parking_capacity(self):
        '''This Function is used to Total parking capacity of the parking lot.'''
        print("Functionality : Check Parking Capacity\n")
        vehicle = Vehicle(self.db)
        vehicle_types = vehicle.fetch_existing_types()
        vehicle_types = [(x[1], x[2]) for x in vehicle_types]
        print(tabulate(vehicle_types, headers=['Slot Type', 'Total Capacity']))

    @access_identifier
    def update_parking_space(self):
        '''This Function is used to update the parking capacity of a vehicle category. 
        It takes vehicle category and new capacity as input and updates the parking capacity.'''
        print("Functionality : Update Parking Space\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        parking_space = ParkingSpace(self.db)
        parking_space.update_parking_space()

    @access_identifier
    def unassign_slot(self):
        '''This Function is used to unassign slot for a vehicle. 
        It takes vehicle number as input and unassigns the slot.'''
        print("Functionality : Unassign Slot\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        slot = Slot(self.db)
        vehicle_number = get_vehicle_number()
        slot.unassign_slot(vehicle_number)

    @access_identifier
    def ban_slot(self):
        '''This Function is used to ban a slot. 
        It takes slot type and slot number as input and bans the slot.'''
        print("Functionality : Ban Slot\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        slot = Slot(self.db)
        slot.ban_slot()

    @access_identifier
    def unban_slot(self):
        '''This Function is used to unban a slot.
        It takes slot number as input and unbans the slot.'''
        print("Functionality : Unban Slot\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        slot = Slot(self.db)
        slot.unban_slot()

    @access_identifier
    def update_parking_charges(self):
        '''This Function is used to update the parking charges of a vehicle category. 
        It takes vehicle category and new charges as input and updates the parking charges.'''
        print("Functionality : Update Parking Charges\n")
        if input("Enter 'q' to exit : \nPress any key continue : ") == 'q':
            return
        parking_space = ParkingSpace(self.db)
        parking_space.update_parking_charges()

    @access_identifier
    def view_ban_slots(self):
        '''This Function is used to view all the banned slots.'''
        print("Functionality : View Ban Slots\n")
        slot = Slot(self.db)
        slot.view_ban_slots()

    def operator_choices(self, choice):
        if choice == 1:
            return Menu.check_parking_capacity
        elif choice == 2:
            return Menu.add_vehicle
        elif choice == 3:
            return Menu.assign_slot
        elif choice == 4:
            return Menu.unassign_slot

    def admin_choices(self, choice):
        if choice == 1:
            return Menu.check_parking_capacity
        elif choice == 2:
            return Menu.add_vehicle_category
        elif choice == 3:
            return Menu.update_parking_space
        elif choice == 4:
            return Menu.update_parking_charges
        elif choice == 5:
            return Menu.ban_slot
        elif choice == 6:
            return Menu.unban_slot
        elif choice == 7:
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
        elif 2 in self.user_details_dict['roles']:
            self.operator_menu()

    def menu_choice_admin(self):
        while True:
            print(prompts.ADMIN_MENU_VIEW)
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
            print(prompts.ADMIN_VIEW)
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
            print(prompts.OPERATOR_VIEW)
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
    db = Database()
    Menu({"name": "Kittu", "user_id": 2, "roles": [1, 2]}, db)
