import unittest
from unittest.mock import MagicMock, patch
from src.controllers.slot import Slot
from src.helpers import helpers
from src.models.database import Database


class TestSlot(unittest.TestCase):

    def setUp(self):
        self.db = MagicMock()
        self.slot = Slot(self.db)
        self.sql_queries = helpers.get_sql_queries()

    def test_ban_slot(self):
        with patch('builtins.input', side_effect=['2', '1']):
            self.slot.fetch_vehicle_types = MagicMock(
                return_value=[('LMV',), ('HMV',), ('Bike',), ('Cycle',)])
            self.slot.all_slots_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            self.slot.display_slot_table_by_category = MagicMock()

            self.slot.check_input_in_range = MagicMock(side_effect=[2, 1])
            self.slot.check_if_slot_already_occupied = MagicMock()

            self.slot.ban_slot()

            self.assertEqual(self.slot.slot_number, 1)
            self.slot.check_input_in_range(
                'Select Vehicle Type To Ban Slot: ', 4)
            self.slot.display_slot_table_by_category.assert_called_with('HMV')
            self.slot.check_input_in_range('Enter Slot Number : ', 2)
            self.slot.check_if_slot_already_occupied.assert_called()
            patch('self.db.update_item', side_effect=[(self.sql_queries["ban_slot"], (1, 'HMV'))])

    def test_unban_slot(self):
        with patch('builtins.input', side_effect=['1']):
            self.slot.view_ban_slots = MagicMock(
                return_value=[(1, 1, 'HMV'), (2, 2, 'LMV')])
            self.slot.check_input_in_range = MagicMock(return_value=1)
            self.db.update_item = MagicMock()
            self.slot.unban_slot()
            self.slot.view_ban_slots.assert_called()
            self.slot.check_input_in_range(
                'Enter Slot Number Index to Unban : ', 2)
            self.db.update_item(self.sql_queries["unban_slot"], (1, 'HMV'))



if __name__ == '__main__':
    unittest.main()
