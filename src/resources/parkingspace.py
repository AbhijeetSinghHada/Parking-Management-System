import traceback
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.helpers.validations import validate_request_data
from src.helpers.entry_menu import Menu
from src.schemas import list_parking_spaces_schema, parking_space_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database

blp = Blueprint("parkingspace", __name__,
                description="Operations on Parking Space")


db = Database()
db_helper = DatabaseHelper(db)
menu_obj = Menu(db)


@blp.route("/parkingspace")
class ParkingSpace(MethodView):

    @jwt_required()
    def get(self):
        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(401, message="Unauthorized")

        try:
            parking_spaces = menu_obj.check_parking_capacity()
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            abort(500, message="An Error Occurred Internally in the Server")
        return parking_spaces

    @jwt_required()
    def put(self):
        jwt = get_jwt()
        if "Admin" not in jwt.get("role"):
            abort(401, message="Unauthorized")

        request_data = request.get_json()
        validation_response = validate_request_data(
            request_data, parking_space_schema)
        if validation_response:
            return validation_response, 400

        try:
            if request_data.get("total_capacity"):
                if request_data.get("total_capacity") < 0:
                    raise ValueError("Total Capacity cannot be less than 0")
                menu_obj.driver_update_parking_space(
                    request_data.get("total_capacity"), request_data.get("slot_type"))
            if request_data.get("charge"):
                if request_data.get("charge") < 0:
                    raise ValueError("Charge cannot be less than 0")
                menu_obj.update_parking_charges(
                    request_data.get("charge"), request_data.get("slot_type"))
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            abort(500, message="An Error Occurred Internally in the Server")
        return request_data

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        if "Admin" not in jwt.get("role"):
            abort(401, message="Unauthorized")

        request_data = request.get_json()
        validation_response = validate_request_data(
            request_data, parking_space_schema)
        if validation_response:
            return validation_response, 400

        try:
            if request_data.get("total_capacity") and request_data.get("charge"):
                menu_obj.driver_add_vehicle_category(
                    request_data.get("slot_type"), request_data.get("total_capacity"), request_data.get("charge"))
            else:
                abort(
                    400, message="Please insert total_capacity and charge fields both.")

        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            abort(500, message="An Error Occurred Internally in the Server")
        return request_data
