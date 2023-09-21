from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.helpers.entry_menu import Menu
from src.schemas import ListParkingSpaceSchema, ParkingSpaceSchema
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database

blp = Blueprint("parkingspace", __name__, description="Operations on Parking Space")


db = Database()
db_helper = DatabaseHelper(db)
menu_obj = Menu(db)


@blp.route("/parkingspace")
class ParkingSpace(MethodView):

    @jwt_required()
    @blp.response(200, ListParkingSpaceSchema(many=True))
    def get(self):
        jwt = get_jwt()
        try:
            parking_spaces = menu_obj.check_parking_capacity()
        except Exception as e:
            abort(400, message=str(e))
        return parking_spaces
    
    @jwt_required()
    @blp.arguments(ParkingSpaceSchema)
    @blp.response(200, ParkingSpaceSchema)
    def put(self, item):
        jwt = get_jwt()
        try:
            if item.get("total_capacity"):
                if item.get("total_capacity") < 0:
                    raise ValueError("Total Capacity cannot be less than 0")
                menu_obj.driver_update_parking_space(item.get("total_capacity"), item.get("slot_type"))
            if item.get("charge"):
                if item.get("charge") < 0:
                    raise ValueError("Charge cannot be less than 0")
                menu_obj.update_parking_charges(item.get("charge"), item.get("slot_type"))
        except Exception as e:
            abort(400, message=str(e))
        return item
    
    @jwt_required()
    @blp.arguments(ParkingSpaceSchema)
    @blp.response(200, ParkingSpaceSchema)
    def post(self, item):
        jwt = get_jwt()
        try:
            if item.get("total_capacity") and item.get("charge"):
                menu_obj.driver_add_vehicle_category(item.get("slot_type"), item.get("total_capacity"), item.get("charge"))
            else:
                raise ValueError("Please insert total_capacity and charge fields both.")
        except Exception as e:
            abort(400, message=str(e))
        return item