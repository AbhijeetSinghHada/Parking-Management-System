from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.helpers.validations import validate_request_data
from src.helpers.entry_menu import Menu
from src.schemas import ban_slot_schema, list_banned_slots_schema, list_slots_status_schema, remove_vehicle_from_slot_schema, slot_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database

blp = Blueprint("slot", __name__, description="Operations on Slot")


db = Database()
db_helper = DatabaseHelper(db)
menu_obj = Menu(db)


@blp.route("/slots")
class Slots(MethodView):

    @jwt_required()
    def post(self):
        """Assign a slot to a vehicle"""
        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(403, message="Forbidden.")

        request_data = request.get_json()
        validation_response = validate_request_data(request_data, slot_schema)
        if validation_response:
            return validation_response, 400

        menu_obj = Menu(db)
        try:
            menu_obj.assign_slot(request_data.get("slot_number"), request_data.get(
                "vehicle_type"), request_data.get("vehicle_number"))
        except Exception as error:
            abort(400, message=str(error))
        return request_data


@blp.route("/slots/<string:slot_type>")
class ListSlots(MethodView):

    @jwt_required()
    def get(self, slot_type):
        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(403, message="Forbidden.")

        try:
            slots = menu_obj.get_slot_table_by_category(slot_type)
            print(slots)
        except Exception as error:
            abort(400, message=str(error))
        return slots


@blp.route("/slots/<string:vehicle_number>")
class RemoveVehicleFromSlot(MethodView):

    @jwt_required()
    def delete(self, vehicle_number):

        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(403, message="Forbidden.")

        try:
            slot_data, bill = menu_obj.unassign_slot(vehicle_number)
            print(slot_data, bill)
            return {"slot": slot_data, "bill": bill}
        except Exception as error:
            abort(400, message=str(error))


@blp.route("/slots/ban")
class BanSlot(MethodView):

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        if "Admin" not in jwt.get("role"):
            abort(403, message="Forbidden.")

        request_data = request.get_json()
        validation_response = validate_request_data(
            request_data, ban_slot_schema)
        if validation_response:
            return validation_response, 400

        try:
            menu_obj.ban_slot(request_data.get("slot_number"),
                              request_data.get("vehicle_type"))
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            abort(500, message="An Error Occurred Internally in the Server")
        return request_data

    @jwt_required()
    def delete(self):
        jwt = get_jwt()
        if "Admin" not in jwt.get("role"):
            abort(403, message="Forbidden.")

        request_data = request.get_json()
        validation_response = validate_request_data(
            request_data, ban_slot_schema)
        if validation_response:
            return validation_response, 400

        try:
            menu_obj.unban_slot(request_data.get("slot_number"),
                                request_data.get("vehicle_type"))
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            abort(500, message="An Error Occurred Internally in the Server")
        return request_data

    @jwt_required()
    def get(self):
        jwt = get_jwt()
        if "Admin" not in jwt.get("role"):
            abort(403, message="Forbidden.")

        try:
            slots = menu_obj.view_ban_slots()
            print(slots)
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            abort(500, message="An Error Occurred Internally in the Server")
        return slots
