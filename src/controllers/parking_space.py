from tabulate import tabulate

from src.controllers.slot import Slot
from src.helpers import helpers, input_and_validation
import logging

logger = logging.getLogger(__name__)
prompts = helpers.get_prompts()


class ParkingSpace(Slot):
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def update_parking_space(self, new_capacity, parking_category):
        logger.debug("update_parking_space called, params - vehicle type : {}, new_capacity : {} ".format(
            parking_category, new_capacity))
        self.db_helper.update_parking_capacity(new_capacity, parking_category)
        print("\nParking Capacity Updated Successfully\n")

    def update_parking_charges(self):
        logger.debug("update_parking_charges called")
        attributes = self.get_parking_slot_attributes()
        parking_category = attributes[0]
        new_charges = input_and_validation.get_int_input(
            'Enter New Charges : ')
        logger.debug("update_parking_charges called, params - vehicle type : {}, new_charges : {} ".format(
            parking_category, new_charges))
        self.db_helper.update_charges(new_charges, parking_category)
        print("\nParking Charges Updated Successfully\n")

    def get_parking_slot_attributes(self):
        vehicle_category_data = self.db_helper.get_vehicle_category_data()
        print(tabulate(vehicle_category_data, headers=[
              'Slot Type', 'Total Capacity', 'Charges'], showindex=range(1, len(vehicle_category_data)+1)))
        update_for_index = helpers.check_input_in_range("Enter the Index of Slot Category : ",
                                                        len(vehicle_category_data))
        parking_category = vehicle_category_data[update_for_index - 1]
        return parking_category

    def are_vehicles_already_parked(self, parking_category, new_capacity):
        slot_data = self.db_helper.get_slots_data()
        for i in slot_data:
            if i[2] == parking_category and i[0] > new_capacity:
                return True
        return False
