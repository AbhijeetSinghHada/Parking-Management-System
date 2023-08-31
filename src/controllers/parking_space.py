from src.controllers.slot import Slot
from src.helpers import helpers, input_and_validation
import logging
logger = logging.getLogger(__name__)


class ParkingSpace(Slot):
    def __init__(self, db):
        super().__init__(db)
        self.db = db

    def update_parking_space(self):
        vehicle_types = self.fetch_existing_types()
        for index, i in enumerate(vehicle_types, start=1):
            print(f"{index}) Slot Type : {i[1]}, Total Capacity : {i[2]}")
        update_for_index = helpers.check_input_in_range("Enter the Index of Slot Category to Add Parking Space : ",
                                                        len(vehicle_types))
        new_capacity = input_and_validation.get_int_input(
            'Enter New Capacity : ')
        if new_capacity <= int(vehicle_types[update_for_index - 1][2]):
            raise ValueError("Enter Capacity Higher then Current.")
        vehicle_type_id = int(vehicle_types[update_for_index - 1][0])
        logger.debug("update_parking_space called, params - vehicle type : {}, new_capacity : {} ".format(
            vehicle_types[update_for_index - 1][0], new_capacity))
        self.update_parking_capacity(new_capacity, vehicle_type_id)
        print("\nParking Capacity Updated Successfully\n")

    def update_parking_capacity(self, total_capacity, category_id):
        logger.debug("update_parking_capacity called with params {},{}".format(
            total_capacity, category_id))
        self.db.update_item(
            self.sql_queries["update_vehicle_capacity"], (total_capacity, category_id))

    def update_parking_charges(self):
        logger.debug("update_parking_charges called")
        vehicle_charges = self.db.get_multiple_items(
            self.sql_queries["get_vehicle_charges"])
        for index, i in enumerate(vehicle_charges, start=1):
            print(f"{index}) Slot Type : {i[1]}, Charges : {i[2]}")
        update_for_index = helpers.check_input_in_range("Enter the Index of Slot Category to Update Charges : ",
                                                        len(vehicle_charges))
        new_charges = input_and_validation.get_int_input(
            'Enter New Charges : ')
        vehicle_type_id = int(vehicle_charges[update_for_index - 1][0])
        logger.debug("update_parking_charges called, params - vehicle type : {}, new_charges : {} ".format(
            vehicle_charges[update_for_index - 1][0], new_charges))
        self.update_charges(new_charges, vehicle_type_id)
        print("\nParking Charges Updated Successfully\n")

    def update_charges(self, charges, category_id):
        logger.debug("update_charges called with params {},{}".format(
            charges, category_id))
        self.db.update_item(
            self.sql_queries["update_vehicle_charges"], (charges, category_id))
