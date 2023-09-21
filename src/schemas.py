from marshmallow import Schema, fields


class CustomerSchema(Schema):
    customer_id = fields.Integer()
    name = fields.String(required=True)
    email_address = fields.Email(required=True)
    phone_number = fields.Integer(required=True)

class VehicleSchema(Schema):
    message = fields.String(dump_only=True)
    vehicle_number = fields.String(required=True)
    vehicle_type = fields.String(required=True)
    customer = fields.Nested(CustomerSchema, required=True)



class SlotsStatusSchema(Schema):
    slot_id = fields.String(required=True, dump_only=True)
    status = fields.String(required=True, dump_only=True)

class ListSlotsStatusSchema(SlotsStatusSchema):
    slots = fields.List(fields.Nested(SlotsStatusSchema), dump_only=True)


class SlotSchema(Schema):
    slot_number = fields.Integer(required=True)
    vehicle_type = fields.String(required=True)
    vehicle_number = fields.String(required=True)

class BillSchema(Schema):
    customer = fields.Nested(CustomerSchema,required = True, dump_only=True)
    time_in = fields.DateTime(required=True, dump_only=True)
    time_out = fields.DateTime(required=True, dump_only=True)
    total_charges = fields.Integer(required=True, dump_only=True)


class RemoveVehicleFromSlot(Schema):
    slot = fields.Nested(SlotSchema, required=True, dump_only=True)
    bill = fields.Nested(BillSchema, required=True, dump_only=True)


class BanSlotSchema(Schema):
    slot_number = fields.Integer(required=True)
    vehicle_type = fields.String(required=True)

class ListBannedSlotsSchema(BanSlotSchema):
    banned_slots = fields.List(fields.Nested(BanSlotSchema), many=True)



class ParkingSpaceSchema(Schema):
    slot_type = fields.String(required=True)
    total_capacity = fields.Integer()
    charge = fields.Integer()

class ListParkingSpaceSchema(ParkingSpaceSchema):
    parking_spaces = fields.List(fields.Nested(ParkingSpaceSchema), many=True)


class UserSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)