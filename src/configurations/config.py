database_url = 'C:\\Users\\ahada\\OneDrive - WatchGuard Technologies Inc\\Parking Management System\\database\\database.db'

connection_parameters = {"host": "127.0.0.1", "user": "root", "password": "2233",
                         "database": "parkingmanagement", "auth_plugin": 'mysql_native_password'}
action_role_mapping = {
    'assign_slot': [1, 2],
    'add_vehicle': [1, 2],
    'driver_add_vehicle_category': [1],
    'check_parking_capacity': [1, 2],
    'driver_update_parking_space': [1],
    'unassign_slot': [1, 2],
    'ban_slot': [1],
    'driver_unban_slot': [1],
    'view_ban_slots': [1],
    'update_parking_charges': [1]
}

prompts_path = "C:\\Users\\ahada\\OneDrive - WatchGuard Technologies Inc\\Parking Management System\\src\\utils\\prompts.json"

sql_queries_path = "C:\\Users\\ahada\\OneDrive - WatchGuard Technologies Inc\\Parking Management System\\src\\utils\\sql_queries.json"
