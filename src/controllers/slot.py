from src.controllers.billing import Billing
from src.helpers import input_and_validation, helpers
from src.utils import sql_queries, prompts
from src.controllers.vehicle import Vehicle
from tabulate import tabulate
from datetime import date, datetime
from src.helpers.helpers import return_no_of_hours_elapsed, return_current_date_time
from src.helpers.input_and_validation import get_vehicle_number


class Slot(Vehicle, Billing):
    def __init__(self, db):
        self.slot_number = None
        self.all_slots_data = None
        self.db = db

    def display_slot_table_by_category(self, vehicle_type):
        slot_data = self.db.get_multiple_items(
            sql_queries.fetch_all_slots_by_category, (vehicle_type,))
        slot_type_capacity = self.db.get_item(
            sql_queries.fetch_capacity_by_slot_types, (vehicle_type,))
        occupied_slot_numbers = [x[0] for x in slot_data]
        self.all_slots_data = []

        for i in range(1, int(slot_type_capacity[0]) + 1):
            if i in occupied_slot_numbers:
                self.all_slots_data.append([i, 'Occupied'])
                continue
            self.all_slots_data.append([i, 'Not Occupied'])
        print(tabulate(self.all_slots_data, headers=['Slot Number', 'Status']))

    def assign_slot(self):
        slot_types = self.fetch_slot_types()
        user_inp = helpers.check_input_in_range('Select Vehicle Type : ', len(slot_types))
        vehicle_type = slot_types[user_inp - 1][0]
        self.display_slot_table_by_category(vehicle_type)
        slot_type_capacity = self.db.get_item(
            sql_queries.fetch_capacity_by_slot_types, (vehicle_type,))
        self.slot_number = helpers.check_input_in_range('Select Slot Number : ', slot_type_capacity[0])
        self.check_if_slot_already_occupied()
        self.vehicle_number = get_vehicle_number()
        if self.db.get_multiple_items(sql_queries.get_slot_by_vehicle_number, (self.vehicle_number,)):
            raise LookupError("Vehicle Already has a slot assigned.")
        data = self.check_if_vehicle_exists(self.vehicle_number)
        if not data:
            print("Vehicle Does not Exist!")
            self.redirect_to_add_vehicle()
        if vehicle_type != self.vehicle_type:
            print("Wrong slot type for vehicle! Try Again.")
            return

        self.set_vehicle_customer_data(data)
        today_date = date.today()
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        self.db.update_item(sql_queries.insert_into_billing_table,
                            (self.vehicle_number, today_date, current_time))
        self.db.update_item(sql_queries.insert_into_slot,
                            (self.slot_number, self.vehicle_number, self.vehicle_type,))
        print("Slot Added Successfully.")

    def redirect_to_add_vehicle(self):
        choice = input(
            "If you want to add Vehicle enter y: \nPress Enter to goto Main Menu : ")
        if choice == 'y' or choice == 'Y':
            self.add_vehicle()
        raise
    def check_if_slot_already_occupied(self):
        if self.all_slots_data[int(self.slot_number) - 1][1] == 'Occupied':
            raise LookupError("Slot Already Occupied! Choose One Which is not.")


    def unassign_slot(self, vehicle_number):
        data = self.db.get_multiple_items(
            sql_queries.get_slot_by_vehicle_number, (vehicle_number,))
        if not data:
            raise LookupError("Slot does not exist. Please First Assign Slot")
        date_time_of_bill = self.db.get_multiple_items(
            sql_queries.get_bill_date_time_from_vehicle_number, (vehicle_number,))
        hours = return_no_of_hours_elapsed(
            date_time_of_bill[0][0], date_time_of_bill[0][1])
        charges = self.db.get_item(
            sql_queries.fetch_charges_from_vehicle_number, (vehicle_number,))[0]

        total_charges = self.calculate_charges(charges, hours)
        datetime_now = return_current_date_time()
        billing_id = self.db.get_item(sql_queries.get_billing_id, (vehicle_number,))
        self.db.update_item(
            sql_queries.update_billing_table, (datetime_now, total_charges, vehicle_number))
        self.db.update_item(sql_queries.delete_parked_slot, (vehicle_number,))
        self.generate_bill(billing_id[0])

    def ban_slot(self):
        slot_types = self.fetch_slot_types()
        user_inp = helpers.check_input_in_range('Select Vehicle Type To Ban Slot: ', slot_types)
        vehicle_type = slot_types[user_inp - 1][0]
        self.display_slot_table_by_category(vehicle_type)
        self.slot_number = input_and_validation.get_int_input("Enter Slot Number : ")
        self.check_if_slot_already_occupied()
        slot_type_capacity = self.db.get_item(
            sql_queries.fetch_capacity_by_slot_types, (vehicle_type,))
        if self.slot_number > int(slot_type_capacity[0]) or self.slot_number < 1:
            print("Slot Number Does not Exist! Choose One Which Does.")
            return
        self.db.update_item(sql_queries.ban_slot,
                            (self.slot_number, vehicle_type))
        print("\nSlot Banned Successfully.\n")

    def view_ban_slots(self):
        data = self.db.get_multiple_items(sql_queries.view_ban_slots)
        data = [(i, x[0], x[1]) for i, x in enumerate(data, start=1)]
        print(tabulate(data, headers=['Index', 'Slot Number', 'Slot Type']))
        return data

    def unban_slot(self):
        data = self.view_ban_slots()
        if not data:
            raise ValueError("No Slots to Unban.")
        slot_number = input_and_validation.get_int_input("Enter Slot Number to Unban : ")
        while slot_number < 1 or slot_number > len(data):
            print("Enter Correct Index Value. \nOut of Range.")
            slot_number = int(input("Enter Slot Number to Unban : "))
        slot_number = data[slot_number - 1][1]
        self.db.update_item(sql_queries.unban_slot, (slot_number,))
        print("\nSlot Unbanned Successfully.\n")


if __name__ == "__main__":
    print("")
