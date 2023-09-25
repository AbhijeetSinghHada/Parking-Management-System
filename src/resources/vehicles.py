from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask import request
from src.helpers.validations import validate_request_data
from src.helpers.entry_menu import Menu
from src.schemas import vehicle_schema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database

blp = Blueprint("vehicle", __name__, description="Operations on Vehicles")


db = Database()
db_helper = DatabaseHelper(db)
menu_obj = Menu(db)


@blp.route("/vehicle")
class Vehicle(MethodView):

    @jwt_required()
    def post(self):
        jwt = get_jwt()
        role = jwt.get("role")
        request_data = request.get_json()
        validation_response = validate_request_data(
            request_data, vehicle_schema)
        if validation_response:
            return validation_response, 400
        if "Admin" not in role and "Operator" not in role:
            abort(401, message="Unauthorized")
        parameters = (request_data.get("vehicle_number"), request_data.get("vehicle_type"),
                      request_data.get("customer").get(
                          "customer_id"), request_data.get("customer").get("name"),
                      request_data.get("customer").get("email_address"), request_data.get("customer").get("phone_number"))
        try:
            data, response = menu_obj.add_vehicle(*parameters)
            data["message"] = response
        except Exception as e:
            abort(500, message=str(e))
        return data
