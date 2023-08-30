import pytest


def test_convert_user_details_to_dict():
    assert convert_user_details_to_dict([['Kittu', 1, 'Admin']]) == {
        'name': 'Kittu', 'user_id': 1, 'roles': ['Admin']}
    assert convert_user_details_to_dict([['Kittu', 1, 'Admin'], ['Kittu', 1, 'Operator']]) == {
        'name': 'Kittu', 'user_id': 1, 'roles': ['Admin', 'Operator']}
    assert convert_user_details_to_dict([['Kittu', 1, 'Admin'], ['Kittu', 1, 'Operator'], ['Kittu', 1, 'Operator']]) == {
        'name': 'Kittu', 'user_id': 1, 'roles': ['Admin', 'Operator', 'Operator']}


def test_check_input_in_range():
    assert check_input_in_range('Enter a number between 1 and 10', 10) == 1
    assert check_input_in_range('Enter a number between 1 and 10', 10) == 10
    assert check_input_in_range('Enter a number between 1 and 10', 10) == 5


def test_return_time_difference():
    assert return_time_difference(
        datetime.now().date(), datetime.now().time()) == 0


def test_return_date_time_combined():
    assert return_date_time_combined(
        datetime.now().date(), datetime.now().time()) == datetime.now()
