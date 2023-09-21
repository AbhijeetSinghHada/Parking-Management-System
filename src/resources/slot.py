from flask_jwt_extended import jwt_required, get_jwt
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.helpers.entry_menu import Menu
from src.schemas import BanSlotSchema, ListBannedSlotsSchema, ListSlotsStatusSchema, SlotSchema, RemoveVehicleFromSlot
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database

blp = Blueprint("slot", __name__, description="Operations on Slot")


db = Database()
db_helper = DatabaseHelper(db)
menu_obj = Menu(db)


@blp.route("/slots")
class Slots(MethodView):


    @jwt_required()
    @blp.arguments(SlotSchema)
    def post(self, item):
        """Assign a slot to a vehicle"""
        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(401, message="Unauthorized")
        menu_obj = Menu(db)
        try:
            menu_obj.assign_slot(item.get("slot_number"),item.get("vehicle_type"),item.get("vehicle_number"))
        except Exception as e:
            abort(400, message=str(e))
        return item


@blp.route("/slots/<string:slot_type>")
class ListSlots(MethodView):

    @jwt_required()
    @blp.response(200, ListSlotsStatusSchema(many=True))
    def get(self, slot_type):
        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(401, message="Unauthorized")
        try:
            slots = menu_obj.get_slot_table_by_category(slot_type)
            print(slots)
        except Exception as e:
            abort(400, message=str(e))
        return slots
    
@blp.route("/slots/<string:vehicle_number>")
class RemoveVehicleFromSlot(MethodView):

    @jwt_required()
    @blp.response(200, RemoveVehicleFromSlot)
    def delete(self, vehicle_number):

        jwt = get_jwt()
        role = jwt.get("role")
        if "Admin" not in role and "Operator" not in role:
            abort(401, message="Unauthorized")
        print(vehicle_number)
        try:
            slot_data, bill = menu_obj.unassign_slot(vehicle_number)
            print(slot_data, bill)
            return {"slot": slot_data, "bill": bill}
        except Exception as e:
            abort(400, message=str(e))


@blp.route("/slots/ban")
class BanSlot(MethodView):
    
    @jwt_required()
    @blp.response(200, SlotSchema)
    @blp.arguments(BanSlotSchema)
    def post(self, item):
        jwt = get_jwt()
        if jwt.get("role") != "Admin":
            abort(401, message="Unauthorized")
        try:
            menu_obj.ban_slot(item.get("slot_number"), item.get("vehicle_type"))
        except Exception as e:
            abort(400, message=str(e))
        return item
    
    @jwt_required()
    @blp.response(200, SlotSchema)
    @blp.arguments(BanSlotSchema)
    def delete(self, item):
        jwt = get_jwt()
        if jwt.get("role") != "Admin":
            abort(401, message="Unauthorized")
        try:
            menu_obj.unban_slot(item.get("slot_number"), item.get("vehicle_type"))
        except Exception as e:
            abort(400, message=str(e))
        return item
    
    @jwt_required()
    @blp.response(200, ListBannedSlotsSchema(many=True))
    def get(self):
        jwt = get_jwt()
        if jwt.get("role") != "Admin":
            abort(401, message="Unauthorized")
        try:
            slots = menu_obj.view_ban_slots()
            print(slots)
        except Exception as e:
            abort(400, message=str(e))
        return slots

