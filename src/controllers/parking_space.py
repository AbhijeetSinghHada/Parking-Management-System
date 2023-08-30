from src.controllers.slot import Slot
from src.helpers import helpers, input_and_validation
from src.utils import sql_queries


class ParkingSpace(Slot):
    def __init__(self,db):
        self.db = db
    def update_parking_space(self):
        vehicle_types = self.fetch_existing_types()
        for index, i in enumerate(vehicle_types, start=1):
            print(f"{index}) Slot Type : {i[1]}, Total Capacity : {i[2]}")
        update_for_index = helpers.check_input_in_range("Enter the Index of Slot Category to Add Parking Space : ",
                                                        len(vehicle_types))
        new_capacity = input_and_validation.get_int_input('Enter New Capacity : ')
        if new_capacity <= int(vehicle_types[update_for_index - 1][2]):
            raise ValueError("Enter Capacity Higher then Current.")
        vehicle_type_id = int(vehicle_types[update_for_index - 1][0])
        self.update_parking_capacity(new_capacity, vehicle_type_id)
        print("\nParking Capacity Updated Successfully\n")

    def update_parking_capacity(self, total_capacity, category_id):
        self.db.update_item(
            sql_queries.update_vehicle_capacity, (total_capacity, category_id))