from unittest.mock import patch

from src.helpers.helpers import convert_user_details_to_dict, check_input_in_range

def test_convert_user_details_to_dict():
    assert convert_user_details_to_dict([['Kittu', 1, 'Admin']]) == {
        'name': 'Kittu', 'user_id': 1, 'roles': ['Admin']}
    assert convert_user_details_to_dict([['Kittu', 1, 'Admin'], ['Kittu', 1, 'Operator']]) == {
        'name': 'Kittu', 'user_id': 1, 'roles': ['Admin', 'Operator']}
    assert convert_user_details_to_dict(
        [['Kittu', 1, 'Admin'], ['Kittu', 1, 'Operator'], ['Kittu', 1, 'Operator']]) == {
               'name': 'Kittu', 'user_id': 1, 'roles': ['Admin', 'Operator', 'Operator']}


def test_check_input_in_range():
    with patch('builtins.input', side_effect=['1','11','10','-1','1']):
        assert check_input_in_range('Enter a number between 1 and 10', 10) == 1
        assert check_input_in_range('Enter a number between 1 and 10', 10) == 10
        assert check_input_in_range('Enter a number between 1 and 10', 10) != 5
