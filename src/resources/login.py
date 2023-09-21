from flask_jwt_extended import create_access_token
from src.controllers.login import Login
from src.schemas import UserSchema
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from src.models.database_helpers import DatabaseHelper
from src.models.database import Database

blp = Blueprint("login", __name__, description="Operations on login")


db = Database()
db_helper = DatabaseHelper(db)

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        
        try:    
            instance = Login(username=user_data["username"], password=user_data["password"], db=db)
            user_id = instance.authenticate()
            print(user_id)
        except Exception as e:
            abort(401, message="Invalid credentials.")
        else:
            user_data = instance.fetch_user_roles()
            access_token = create_access_token(identity=user_data.get("user_id"), additional_claims=user_data)
            return {"access_token": access_token}, 200
