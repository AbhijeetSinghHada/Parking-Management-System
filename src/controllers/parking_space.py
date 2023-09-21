from tabulate import tabulate
from Parking_Management_System.src.helpers import validations

from src.controllers.slot import Slot
from src.helpers import helpers
import logging

logger = logging.getLogger(__name__)
prompts = helpers.get_prompts()


class ParkingSpace(Slot):
    def __init__(self, db_helper):
        self.db_helper = db_helper

    def update_parking_capacity(self, new_capacity, parking_category):
        logger.debug("update_parking_space called, params - vehicle type : {}, new_capacity : {} ".format(
            parking_category, new_capacity))
        self.db_helper.update_parking_capacity(new_capacity, parking_category)
        print("\nParking Capacity Updated Successfully\n")

    def update_parking_charges(self, new_charges, parking_category):
        
        self.db_helper.update_charges(new_charges, parking_category)
        print("\nParking Charges Updated Successfully\n")

    def get_parking_slot_attributes(self, parking_category):
        vehicle_category_data = self.db_helper.get_vehicle_category_data()
        print(vehicle_category_data)
        parking_category_data = None
        for i in vehicle_category_data:
            if parking_category == i[0]:
                parking_category_data = i
        return parking_category_data

    def are_vehicles_already_parked(self, parking_category, new_capacity):
        slot_data = self.db_helper.get_slots_data()
        for i in slot_data:
            if i[2] == parking_category and i[0] > new_capacity:
                return True
        return False
