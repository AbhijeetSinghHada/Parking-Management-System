

data = {
    "name": "Abhijeet",
    "email_address": "abhi22hada@gmail.com",
    "phone_number": 1234567890,
    "vehicle_number": "MH01AB1234",
    "vehicle_type": "LMV"
}

response_data = {
    "message": "Vehicle Added Successfully",
    "vehicle_id": 1,
    "customer_id": 1
}

reqest_schema = {
    "name": "str",
    "email_address": "str",
    "phone_number": "int",
    "vehicle_number": "str",
    "vehicle_type": "str"
}

response_schema = {
    "message": "str",
    "vehicle_id": "int",
    "customer_id": "int"
}
# get response

def validate_data_by_schema(data, schema):
    for key, value in schema.items():
        try:
            if type(data[key]).__name__ != value:
                raise Exception(f"Invalid Data Type for {key}")
        except KeyError:
            raise Exception(f"Missing Key {key}")
        except Exception as e:
            raise Exception(str(e))

# msg
# errorcode
# description

def validate_request(schema):
    def hello(func):

        def function(data):
            validate_data_by_schema(data, schema)
            response_data = func(data)
            return response_data
        return function
    return hello


def validate_response(schema):
    def hello(func):

        def function(data):
            response_data = func(data)
            validate_data_by_schema(response_data, schema)
            return response_data
        return function
    return hello


@validate_request(reqest_schema)
def func(data):

    return response_data


try:
    dat = func(data)
except Exception as e:
    print(e)
