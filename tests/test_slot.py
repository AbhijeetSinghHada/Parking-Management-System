import unittest
from unittest import mock
from unittest.mock import Mock, MagicMock
from src.controllers.slot import Slot


class TestSlot(unittest.TestCase):

    def setUp(self):
        self.db_helper = Mock()
        self.slot = Slot(self.db_helper)

    def test_display_slot_table_by_category(self):
        self.db_helper.get_slots_data.return_value = [(1, 'RJ20CD7259', 'LMV'), (2, 'RJ20CD7259', 'LMV'), (3, 'RJ20CD7259', 'LMV'), (4, 'RJ20CD7259', 'LMV'), (5, 'RJ20CD7259', 'LMV'), (6, 'RJ20CD7259', 'LMV'), (7, 'RJ20CD7259', 'LMV'), (8, 'RJ20CD7259', 'LMV'), (9, 'RJ20CD7259', 'LMV'), (
            10, 'RJ20CD7259', 'LMV'), (11, 'RJ20CD7259', 'LMV'), (12, 'RJ20CD7259', 'LMV'), (13, 'RJ20CD7259', 'LMV'), (14, 'RJ20CD7259', 'LMV'), (15, 'RJ20CD7259', 'LMV'), (16, 'RJ20CD7259', 'LMV'), (17, 'RJ20CD7259', 'LMV'), (18, 'RJ20CD7259', 'LMV'), (19, 'RJ20CD7259', 'LMV'), (20, 'RJ20CD7259', 'LMV')]
        self.db_helper.get_parking_capacity.return_value = 20
        self.slot.display_slot_table_by_category('LMV')
        self.db_helper.get_slots_data.assert_called_once()
        self.db_helper.get_parking_capacity.assert_called_once()

    def test_assign_slot(self):
        self.db_helper.insert_into_slot_table.return_value = None
        self.slot.assign_slot(1, 'RJ20CD7259', 'LMV')
        self.db_helper.insert_into_slot_table.assert_called_once()

    def test_check_if_slot_already_occupied(self):
        self.db_helper.get_slots_data.return_value = [(1, 'RJ20CD7259', 'LMV'), (2, 'RJ20CD7259', 'LMV'), (3, 'RJ20CD7259', 'LMV'), (4, 'RJ20CD7259', 'LMV'), (5, 'RJ20CD7259', 'LMV'), (6, 'RJ20CD7259', 'LMV'), (7, 'RJ20CD7259', 'LMV'), (8, 'RJ20CD7259', 'LMV'), (9, 'RJ20CD7259', 'LMV'), (
            10, 'RJ20CD7259', 'LMV'), (11, 'RJ20CD7259', 'LMV'), (12, 'RJ20CD7259', 'LMV'), (13, 'RJ20CD7259', 'LMV'), (14, 'RJ20CD7259', 'LMV'), (15, 'RJ20CD7259', 'LMV'), (16, 'RJ20CD7259', 'LMV'), (17, 'RJ20CD7259', 'LMV'), (18, 'RJ20CD7259', 'LMV'), (19, 'RJ20CD7259', 'LMV'), (20, 'RJ20CD7259', 'LMV')]

        with self.assertRaises(LookupError):
            self.slot.check_if_slot_already_occupied(1, 'LMV')

    def test_unassign_slot(self):
        self.db_helper.remove_parked_slot.return_value = None
        self.slot.unassign_slot(1)
        return_val = self.db_helper.remove_parked_slot(1)
        self.assertEqual(return_val, None)

    def test_ban_slot(self):
        self.db_helper.ban_slot_by_slot_number.return_value = None
        self.slot.ban_slot(1, 'LMV')
        return_val = self.db_helper.ban_slot_by_slot_number(1, 'LMV')
        self.assertEqual(return_val, None)

    def test_view_ban_slots_positive(self):
        self.db_helper.get_slots_data.return_value = [(1, -1, 'LMV'), (2, 'RJ20CD7259', 'LMV'), (3, 'RJ20CD7259', 'LMV'), (
            4, 'RJ20CD7259', 'LMV'), (5, 'RJ20CD7259', 'LMV'), (6, 'RJ20CD7259', 'LMV'), (7, -1, 'LMV'), (8, 'RJ20CD7259', 'LMV')]
        self.slot.view_ban_slots()
        self.db_helper.get_slots_data.assert_called_once()

    def test_view_ban_slots_negative(self):
        self.db_helper.get_slots_data.return_value = [(1, 'RJ20CD7259', 'LMV'), (2, 'RJ20CD7259', 'LMV'), (3, 'RJ20CD7259', 'LMV'), (
            4, 'RJ20CD7259', 'LMV'), (5, 'RJ20CD7259', 'LMV'), (6, 'RJ20CD7259', 'LMV'), (7, 'RJ20CD7259', 'LMV'), (8, 'RJ20CD7259', 'LMV')]
        with self.assertRaises(ValueError):
            self.slot.view_ban_slots()

    def test_unban_slot(self):
        self.db_helper.unban_slot.return_value = None
        self.slot.unban_slot(1, 'LMV')
        return_val = self.db_helper.unban_slot(1, 'LMV')
        self.assertEqual(return_val, None)


if __name__ == '__main__':
    unittest.main()
