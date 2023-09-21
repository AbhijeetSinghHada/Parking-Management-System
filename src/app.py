import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from src.resources.slot import blp as SlotsBlueprint
from src.resources.parkingspace import blp as ParkingSpaceBlueprint
from src.resources.login import blp as LoginBlueprint
from src.resources.vehicles import blp as VehiclesBlueprint


def create_app():
    app = Flask(__name__)

    app.config["PROPOGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Park+ Parking Management System REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    api = Api(app)

    app.config["JWT_SECRET_KEY"] = "abhi"
    jwt = JWTManager(app)

    api.register_blueprint(SlotsBlueprint)
    api.register_blueprint(LoginBlueprint)
    api.register_blueprint(ParkingSpaceBlueprint)
    api.register_blueprint(VehiclesBlueprint)

    return app
