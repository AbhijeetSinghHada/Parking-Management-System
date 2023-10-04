import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
authroization_header ="Bearer " + os.getenv("bearer_token")

from src.app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app
2

@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_parkingspace_get_valid_response(client):
    response = client.get("/parkingspace", headers={"Authorization": authroization_header})
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert isinstance(response.json[0], dict)
    assert response.json[0].get("slot_type")
    assert response.json[0].get("total_capacity")
    assert response.json[0].get("charge")


def test_parkingspace_post_missing_field(client):
    response = client.post("/parkingspace", headers={"Authorization": authroization_header}, json={"slot_type": "Car", "charge": 100})
    assert response.status_code == 400
    assert isinstance(response.json, dict)
    assert response.json == {
    "code": 400,
    "message": "'total_capacity' is a required property",
    "status": "Bad Request"
}
    
def test_parkingspace_post_invalid_field(client):
    response = client.post("/parkingspace", headers={"Authorization": authroization_header}, json={"slot_type": "Car", "total_capacity": -100, "charge": 10})
    assert response.status_code == 400
    assert isinstance(response.json, dict)
    assert response.json == {
    "code": 400,
    "message": "Invalid Integer Input.",
    "status": "Bad Request"
}
    
def test_parkingspace_put_valid_response(client):
    response = client.put("/parkingspace", headers={"Authorization": authroization_header}, json={"slot_type": "Car", "total_capacity": 100, "charge": 10})
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json.get("slot_type")
    assert response.json.get("total_capacity")
    assert response.json.get("charge")

def test_parkingspace_put_missing_field(client):
    response = client.put("/parkingspace", headers={"Authorization": authroization_header}, json={})
    assert response.status_code == 400
    assert isinstance(response.json, dict)
    assert response.json == {
    "code": 400,
    "message": "'slot_type' is a required property",
    "status": "Bad Request"
}

def test_parkingspace_put_invalid_capacity(client):
    response = client.put("/parkingspace", headers={"Authorization": authroization_header}, json={"slot_type": "Car", "total_capacity": -100, "charge": 10})
    assert response.status_code == 400
    assert isinstance(response.json, dict)
    assert response.json == {
    "code": 400,
    "message": "Total Capacity cannot be less than 0",
    "status": "Bad Request"
}
    
def test_parkingspace_put_invalid_slot_type(client):
    response = client.put("/parkingspace", headers={"Authorization": authroization_header}, json={"slot_type": "NotValidType", "total_capacity": 100, "charge": 10})
    assert response.status_code == 400
    assert isinstance(response.json, dict)
    assert response.json == {
    "code": 400,
    "message": "No Parking Space Exists for this Category",
    "status": "Bad Request"
}