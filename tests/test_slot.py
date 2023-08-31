import unittest
from unittest.mock import MagicMock, patch
from src.controllers.slot import Slot
from src.helpers import helpers
from src.models.database import Database


class TestSlot(unittest.TestCase):

    def setUp(self):
        self.db = Database()
        self.slot = Slot(self.db)
        self.sql_queries = helpers.get_sql_queries()
        self.slot.helpers = MagicMock()
        self.slot.helpers.check_input_in_range = MagicMock()
    def test_ban_slot(self):
        with patch('builtins.input', side_effect=['2', '1']):
            self.slot.fetch_slot_types = MagicMock(return_value=[('LMV',), ('HMV',), ('Bike',), ('Cycle',)])
            self.slot.all_slots_data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            self.slot.display_slot_table_by_category = MagicMock()

            helpers.check_input_in_range = MagicMock(return_value=4)
            self.slot.check_if_slot_already_occupied = MagicMock()

            self.slot.ban_slot()

            self.assertEqual(self.slot.slot_number, 1)
            self.slot.helpers.check_input_in_range('Select Vehicle Type To Ban Slot: ',4)
            self.slot.display_slot_table_by_category.assert_called_with('HMV')
            self.slot.helpers.check_input_in_range.assert_called_with('Enter Slot Number : ', 2)
            self.slot.check_if_slot_already_occupied.assert_called()
            assert self.db.update_item(self.sql_queries["ban_slot"],
                                                        (1, 'HMV'))


if __name__ == '__main__':
    unittest.main()
