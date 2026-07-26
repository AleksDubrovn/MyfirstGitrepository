import requests
import pytest


BASE_URL = "https://petstore3.swagger.io/api/v3"

@pytest.fixture(scope="function")
def create_pet():
    payload = {"id": 1,
               "name": "Nick",
               "status": "available"
               }
    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()

