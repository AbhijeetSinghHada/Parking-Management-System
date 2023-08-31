import functools
from src.configurations.config import action_role_mapping
from src.helpers.errors import AccessDenied
import logging
logger = logging.getLogger(__name__)

def access_identifier(function):
    @functools.wraps(function)
    def access_function(*args, **kwargs):
        user_details_dict = args[0].user_details_dict
        if any(x in action_role_mapping[function.__name__] for x in user_details_dict['roles']):
            return_value = function(*args, **kwargs)
            return return_value
        raise AccessDenied("\nYour Role Do not Have Access to this Function.\n")

    return access_function

if __name__ == '__main__':
    print('')