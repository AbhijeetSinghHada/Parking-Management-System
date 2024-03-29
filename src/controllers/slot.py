import logging
from tabulate import tabulate
from src.controllers.billing import Billing
from src.controllers.vehicle import Vehicle
from src.helpers.helpers import get_sql_queries
logger = logging.getLogger(__name__)


class Slot(Vehicle, Billing):
    def __init__(self, db_helper):
        self.sql_queries = get_sql_queries()
        self.slot_number = None
        self.db_helpers = db_helper

    def display_slot_table_by_category(self, vehicle_type):
        logger.debug("display_slot_table_by_category called with params {}".format(
            vehicle_type))
        slot_data = self.db_helpers.get_slots_data()
        slot_type_capacity = self.db_helpers.get_parking_capacity(vehicle_type)

        occupied_slot_numbers = [x[0]
                                 for x in slot_data if x[2] == vehicle_type]
        all_slots_data = []

        for i in range(1, int(slot_type_capacity) + 1):
            if i in occupied_slot_numbers:
                all_slots_data.append([i, 'Occupied'])
                continue
            all_slots_data.append([i, 'Not Occupied'])
        print(tabulate(all_slots_data, headers=['Slot Number', 'Status']))

    def assign_slot(self, slot_number, vehicle_number, vehicle_type):
        logger.debug("assign_slot called")

        self.db_helpers.insert_into_slot_table(slot_number, vehicle_number, vehicle_type)
        print("Slot Added Successfully.")

    def check_if_slot_already_occupied(self, slot_number, slot_type):
        logger.debug(
            "check_if_slot_already_occupied called with params {}, {}".format
            (slot_number, slot_type))
        slot_data = self.db_helpers.get_slots_data()
        slot_data_by_type = [x[0] for x in slot_data if x[2] == slot_type]
        if slot_number in slot_data_by_type:
            raise LookupError(
                "Slot Already Occupied! Choose One Which is not.")

    def unassign_slot(self, slot_id):
        logger.debug("unassign_slot called with params {}".format(
            slot_id))

        self.db_helpers.remove_parked_slot(slot_id)

    def ban_slot(self, slot_number, vehicle_type):
        logger.debug("ban_slot called")
        self.db_helpers.ban_slot_by_slot_number(slot_number, vehicle_type)
        print("\nSlot Banned Successfully.\n")

    def view_ban_slots(self):
        logger.debug("view_ban_slots called")
        data = self.db_helpers.get_slots_data()
        data = [(x[0], x[2]) for x in data if x[1] == -1]
        if not data:
            raise ValueError("\nNo Banned Slots.\n")
        print(tabulate(data, headers=['Slot Number', 'Slot Type'], showindex=range(1, len(data) + 1)))
        return data

    def unban_slot(self, slot_number, slot_type):
        logger.debug("unban_slot called")

        self.db_helpers.unban_slot(slot_number, slot_type)
        print("\nSlot Unbanned Successfully.\n")


if __name__ == "__main__":
    print("")
