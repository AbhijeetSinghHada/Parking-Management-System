fetch_login_details = "SELECT * FROM parkingmanagement.credentials WHERE username = %s and password = %s"
insert_login_details = ''
fetch_user_details = "SELECT e.emp_name,e.id,r.id FROM parkingmanagement.employee as e inner join parkingmanagement.role_mapping as m on e.id = m.user_id inner join parkingmanagement.roles as r on m.role_id = r.id where e.id= %s "

fetch_vehicle_types = "SELECT * FROM parkingmanagement.slot_category"
add_vehicle_type = "INSERT INTO `parkingmanagement`.`slot_category` (`slot_type`, `total_capacity`) VALUES (%s,%s)"
add_to_charges_tables = "INSERT INTO `parkingmanagement`.`charges` SET slot_category_id = last_insert_id(), charge = %s"
update_vehicle_capacity = "UPDATE `parkingmanagement`.`slot_category` SET `total_capacity` = %s WHERE (`id` = %s)"

fetch_slot_types = "SELECT slot_type FROM parkingmanagement.slot_category"
fetch_capacity_by_slot_types = "SELECT total_capacity FROM parkingmanagement.slot_category where slot_type = %s"
fetch_vehicle_data = "SELECT c.id,c.customer_name,c.email,c.phone_number, v.vehicle_number, s.slot_type FROM parkingmanagement.customer as c inner join parkingmanagement.vehicle as v on c.id = v.customer_id inner join parkingmanagement.slot_category as s on v.slot_category_id = s.id where v.vehicle_number=%s or c.id=%s or c.email=%s;"
fetch_customer_data = "SELECT * FROM parkingmanagement.customer where id=%s or email=%s or phone_number=%s;"
insert_vehicle_by_customer_by_email_or_phone = """INSERT INTO parkingmanagement.vehicle SET customer_id = 
( SELECT id FROM parkingmanagement.customer WHERE email = %s or phone_number=%s ),
vehicle_number = %s, slot_category_id = (SELECT id FROM parkingmanagement.slot_category WHERE slot_type = %s)"""
insert_vehicle_by_customer_id = """INSERT INTO parkingmanagement.vehicle SET customer_id = %s,
vehicle_number = %s, slot_category_id = (SELECT id FROM parkingmanagement.slot_category WHERE slot_type = %s)"""

insert_customer = "INSERT INTO parkingmanagement.customer(customer_name,email,phone_number) values(%s,%s,%s)"
insert_vehicle = """INSERT INTO parkingmanagement.vehicle SET customer_id = last_insert_id(),
vehicle_number = %s, slot_category_id = (SELECT id FROM parkingmanagement.slot_category WHERE slot_type = %s)"""

fetch_all_slots_by_category = """SELECT s.slot_number,s.vehicle_id,s.status_id, c.slot_type, c.total_capacity 
FROM parkingmanagement.slot  as s 
inner join parkingmanagement.slot_category as c on s.slot_category_id = c.id 
where s.slot_category_id= (SELECT id FROM parkingmanagement.slot_category WHERE slot_type = %s)"""

insert_into_billing_table = "INSERT INTO parkingmanagement.billing SET \
vehicle_id = ( SELECT id FROM parkingmanagement.vehicle WHERE vehicle_number=%s), \
bill_date = %s, time_parked_in = %s"

insert_into_slot = """INSERT INTO parkingmanagement.slot SET billing_id = last_insert_id(),
slot_number = %s, vehicle_id = ( SELECT id FROM parkingmanagement.vehicle WHERE vehicle_number=%s), 
slot_category_id = (SELECT id FROM parkingmanagement.slot_category WHERE slot_type = %s),
status_id ='2'"""

get_bill_date_time_from_vehicle_number = "Select bill_date, time_parked_in from parkingmanagement.billing\
 where id = (select billing_id from parkingmanagement.slot where \
 vehicle_id = (select id from parkingmanagement.vehicle where vehicle_number=%s))"

fetch_charges_from_vehicle_number = "SELECT charge FROM parkingmanagement.charges where \
slot_category_id=(select slot_category_id from parkingmanagement.vehicle where vehicle_number=%s)"

update_billing_table = "UPDATE parkingmanagement.billing set date_time_parked_out=%s,\
 total_charges=%s where id = (select billing_id from parkingmanagement.slot \
 where vehicle_id = (select id from parkingmanagement.vehicle where vehicle_number=%s))"

delete_parked_slot = "DELETE from parkingmanagement.slot where vehicle_id = \
(select id from parkingmanagement.vehicle where vehicle_number=%s)"

get_billing_id = """SELECT billing_id from parkingmanagement.slot
where vehicle_id = (select id from parkingmanagement.vehicle where vehicle_number=%s)"""

get_billing_details = """
SELECT bill.id, c.id,c.customer_name,c.email,c.phone_number, v.vehicle_number, s.slot_type,
bill.bill_date, bill.time_parked_in, bill.date_time_parked_out, bill.total_charges
FROM parkingmanagement.customer as c
inner join parkingmanagement.vehicle as v
on c.id = v.customer_id
inner join parkingmanagement.slot_category as s
on v.slot_category_id = s.id
inner join parkingmanagement.billing as bill
on v.id = bill.vehicle_id
where bill.id = %s"""

get_slot_by_vehicle_number = """SELECT id from parkingmanagement.slot where vehicle_id = 
(SELECT id from parkingmanagement.vehicle where vehicle_number=%s)"""


ban_slot = """INSERT INTO parkingmanagement.slot SET billing_id = '-1',
slot_number = %s, vehicle_id = '-1', 
slot_category_id = (SELECT id FROM parkingmanagement.slot_category WHERE slot_type = %s),
status_id = '1'"""

view_ban_slots = """SELECT s.slot_number, c.slot_type FROM parkingmanagement.slot as s
inner join parkingmanagement.slot_category as c
on s.slot_category_id = c.id"""

unban_slot = """DELETE from parkingmanagement.slot where slot_number = %s"""
