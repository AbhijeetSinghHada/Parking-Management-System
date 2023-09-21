from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.helpers.entry_menu import Menu
from src.schemas import VehicleSchema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database

blp = Blueprint("vehicle", __name__, description="Operations on Vehicles")


db = Database()
db_helper = DatabaseHelper(db)
menu_obj = Menu(db)


@blp.route("/vehicle")
class Vehicle(MethodView):

    @jwt_required()
    @blp.response(200, VehicleSchema)
    @blp.arguments(VehicleSchema)
    def post(self, item):
        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(401, message="Unauthorized")
        parameters = (item.get("vehicle_number"), item.get("vehicle_type"),item.get("customer").get("customer_id"), item.get("customer").get("name"), item.get("customer").get("email_address"), item.get("customer").get("phone_number")) 
        try:
            data, response = menu_obj.add_vehicle(*parameters)
            data["message"] = response
        except Exception as e:
            abort(400, message=str(e))
        return data