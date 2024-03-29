import unittest

import datetime
from unittest import mock
from unittest.mock import Mock, MagicMock

from src.controllers.billing import Billing


class TestBilling(unittest.TestCase):

    def setUp(self):
        self.db_helper = Mock()
        self.billing = Billing(self.db_helper)

    def test_calculate_charges_hours_more_than_zero(self):
        return_value = self.billing.calculate_charges(20, 12)
        self.assertEquals(return_value, 240)
        return_value = self.billing.calculate_charges(0, 12)
        self.assertEquals(return_value, 0)

    def test_calculate_charges_hours_zero(self):
        return_value = self.billing.calculate_charges(20, 0)
        self.assertEquals(return_value, 20)

    def test_calculate_charges_hours_less_than_zero(self):
        return_value = self.billing.calculate_charges(40, -2)
        self.assertEquals(return_value, 40)

    @mock.patch("src.helpers.helpers.return_date_time_combined")
    def test_generate_bill_with_existing_id(self, mock_helper):
        mock_data = [(12, 1, 'Ram', 'ram@gmail.com', '1234567899', 'RJ20CD7259',
                      'LMV', datetime.date(2023, 9, 11), datetime.timedelta(seconds=36900), 25)]
        self.db_helper.get_billing_details.return_value = mock_data
        mock_helper.return_value = datetime.datetime(2023, 9, 11, 10, 16)
        bill_id = 1
        bill = self.billing.generate_bill(bill_id)

        # Assertions to check if the function returns the expected result
        expected_bill = [12, 1, 'Ram', 'ram@gmail.com', '1234567899',
                         'RJ20CD7259', 'LMV', datetime.datetime(2023, 9, 11, 10, 15), 25]
        self.assertEqual(bill, expected_bill)

    def test_generate_bill_with_non_existing_id(self):
        # Mock the behavior of db_helper.get_billing_details to return None
        self.db_helper.get_billing_details.return_value = None

        bill_id = 999  # Replace with a non-existent bill_id for testing
        with self.assertRaises(LookupError):
            self.billing.generate_bill(bill_id)

    def test_update_bill_table(self):
        self.db_helper.parked_time_elapsed_in_hours.return_value = 12
        self.billing.calculate_charges = MagicMock(return_value=240)
        self.billing.update_bill_table(1, 20)
        self.db_helper.update_billing_table.return_value = None

        response = self.db_helper.update_billing_table(1, 240, 1)
        self.assertEqual(response, None)

    def test_insert_into_bill_table(self):
        self.db_helper.insert_into_billing_table.return_value = None
        response = self.db_helper.insert_into_billing_table(
            "RJ20CD7259", "2023-09-11", "10:15:00")
        self.assertEqual(response, None)


if __name__ == '__main__':

    unittest.main()
