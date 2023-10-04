import dotenv
import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.app import create_app
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

def test_user_login(client):
    response = client.post("/login", json={"username": "abhi", "password": "Abhi2233"})
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert response.json.get("access_token")

    os.environ["bearer_token"] =  response.json.get("access_token")
    dotenv.set_key(dotenv_file, "bearer_token", os.environ["bearer_token"])


