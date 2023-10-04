import traceback
from flask_jwt_extended import jwt_required, get_jwt
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.helpers.validations import validate_request_data
from src.helpers.driver_program import ProgramDriver
from src.schemas import ban_slot_schema, slot_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database
import logging
logger = logging.getLogger(__name__)
blp = Blueprint("slot", __name__, description="Operations on Slot")


db = Database()
db_helper = DatabaseHelper(db)
menu_obj = ProgramDriver(db)


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

        menu_obj = ProgramDriver(db)
        try:
            menu_obj.assign_slot(request_data.get("slot_number"), request_data.get(
                "vehicle_type"), request_data.get("vehicle_number"))
            return request_data
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: Slots(MethodView) Method: post() Traceback: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: Slots(MethodView) Method: post() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")
        


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
            return slots
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: ListSlots(MethodView) Method: get() Traceback: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: ListSlots(MethodView) Method: get() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")
        


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
            return {"slot": slot_data, "bill": bill}
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: RemoveVehicleFromSlot(MethodView) Method: delete() Traceback: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: RemoveVehicleFromSlot(MethodView) Method: delete() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")


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
            abort(400, message=validation_response)

        try:
            menu_obj.ban_slot(request_data.get("slot_number"),
                              request_data.get("vehicle_type"))
            return request_data
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: BanSlot(MethodView) Method: post() Traceback: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: BanSlot(MethodView) Method: post() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")
        

    @jwt_required()
    def delete(self):
        jwt = get_jwt()
        if "Admin" not in jwt.get("role"):
            abort(403, message="Forbidden.")

        request_data = request.get_json()
        validation_response = validate_request_data(
            request_data, ban_slot_schema)
        if validation_response:
            abort(400, message=validation_response)

        try:
            menu_obj.unban_slot(request_data.get("slot_number"),
                                request_data.get("vehicle_type"))
            return request_data
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: BanSlot(MethodView) Method: delete() Traceback: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: BanSlot(MethodView) Method: delete() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")
        

    @jwt_required()
    def get(self):
        jwt = get_jwt()
        if "Admin" not in jwt.get("role"):
            abort(403, message="Forbidden.")

        try:
            slots = menu_obj.view_ban_slots()
            return slots
        except LookupError as error:
            abort(409, message=str(error))
        except ValueError as error:
            abort(400, message=str(error))
        except Exception as error:
            logger.debug("Error Occurred: BanSlot(MethodView) Method: get() Traceback: {}".format(
                traceback.format_exc()))
            logger.error("Error Occurred: BanSlot(MethodView) Method: get() Error: {}".format(
                str(error)))
            abort(500, message="An Error Occurred Internally in the Server")
        
