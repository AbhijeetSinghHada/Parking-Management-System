from unittest import mock, TestCase

from src.helpers import input_and_validation


class TestInputAndValidation(TestCase):

    def test_get_username_input_correct(self):
        with mock.patch('builtins.input', return_value='test_user'):
            assert input_and_validation.get_username_input() == 'test_user'

    def test_get_username_input_incorrect(self):
        with mock.patch('builtins.input', side_effect=['test_user@#', 'test_user1']):
            assert input_and_validation.get_username_input() == 'test_user1'

    def test_get_customer_id_correct(self):
        with mock.patch('builtins.input', return_value='123456'):
            assert input_and_validation.get_customer_id(
                'Enter Customer ID : ') == '123456'

    def test_get_customer_id_incorrect(self):
        with mock.patch('builtins.input', side_effect=['123456@#', '123456']):
            assert input_and_validation.get_customer_id(
                'Enter Customer ID : ') == '123456'

    def test_get_vehicle_number_correct(self):
        with mock.patch('builtins.input', return_value='RJ20CD7259'):
            assert input_and_validation.get_vehicle_number() == 'RJ20CD7259'

    def test_get_vehicle_number_incorrect(self):
        with mock.patch('builtins.input', side_effect=['RJ20CD7259@#', 'RJ20CD7259']):
            assert input_and_validation.get_vehicle_number() == 'RJ20CD7259'

    def test_get_int_input_correct(self):
        with mock.patch('builtins.input', return_value='123456'):
            assert input_and_validation.get_int_input(
                'Enter Integer : ') == 123456

    def test_get_int_input_incorrect(self):
        with mock.patch('builtins.input', side_effect=['123456@#', '123456']):
            assert input_and_validation.get_int_input(
                'Enter Integer : ') == 123456

    def test_get_string_input_correct(self):
        with mock.patch('builtins.input', return_value='test'):
            assert input_and_validation.get_string_input(
                'Enter String : ') == 'test'

    def test_get_string_input_incorrect(self):
        with mock.patch('builtins.input', side_effect=['test@#', 'test']):
            assert input_and_validation.get_string_input(
                'Enter String : ') == 'test'

    def test_input_validate_password_correct(self):
        with mock.patch('src.helpers.input_and_validation.maskpass.askpass', return_value='Abhi@123'):
            assert input_and_validation.input_validate_password() == 'Abhi@123'

    def test_input_validate_password_incorrect(self):
        with mock.patch('src.helpers.input_and_validation.maskpass.askpass', side_effect=['test', 'Abhi@123']):
            assert input_and_validation.input_validate_password() == 'Abhi@123'

    def test_input_validate_phone_number_correct(self):
        with mock.patch('builtins.input', return_value='9602606500'):
            assert input_and_validation.input_validate_phone_number(
                'Enter Phone Number : ') == 9602606500

    def test_input_validate_phone_number_incorrect(self):
        with mock.patch('builtins.input', side_effect=['9602606500@#', '9602606500']):
            assert input_and_validation.input_validate_phone_number(
                'Enter Phone Number : ') == 9602606500

    def test_input_validate_email_correct(self):
        with mock.patch('builtins.input', side_effect=['abhi@gmail.com']):
            assert input_and_validation.input_validate_email(
                "Enter Email ID : ") == 'abhi@gmail.com'

    def test_input_validate_email_incorrect(self):
        with mock.patch('builtins.input', side_effect=['a@g.c', 'abhi@gmail.com']):
            assert input_and_validation.input_validate_email(
                "Enter Email ID : ") == 'abhi@gmail.com'
