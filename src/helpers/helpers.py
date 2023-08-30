import json
from datetime import datetime

from src.helpers import input_and_validation


def dump_roles_to_cache(user_data):
    with open(
            'C:\\Users\\ahada\\OneDrive - WatchGuard Technologies Inc\\Parking Management System\\src\\configurations\\cache.txt',
            'w') as fp:
        json.dump(user_data, fp)


def convert_user_details_to_dict(lst):
    user_dict = {'name': lst[0][0],
                 'user_id': lst[0][1],
                 'roles': [x[2] for x in lst]}
    return user_dict


def check_input_in_range(message, comparison_category):
    user_inp = input_and_validation.get_int_input(message)
    while user_inp >comparison_category or user_inp < 1:
        user_inp = input_and_validation.get_int_input(f'Please Enter valid index: ')
    return user_inp


def return_time_difference(_date, _time):
    print(_time)
    _time = (datetime.min + _time).time()
    tdelta = (datetime.now() - datetime.combine(_date, _time))
    return tdelta


def return_date_time_combined(_date, _time):
    _time = (datetime.min + _time).time()
    return datetime.combine(_date, _time)


def return_no_of_hours_elapsed(date_data, time_data):
    tdelta = return_time_difference(date_data, time_data)
    return int(str(tdelta).split(':')[0])


def return_current_date_time():
    datetime_now = datetime.now()
    return datetime_now.strftime("%Y-%m-%d %H:%M")
