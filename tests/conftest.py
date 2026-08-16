import requests
import pytest
import random
import tests.shemas

BASE_URL = "http://5.181.109.28:9090/api/v3"

@pytest.fixture(scope="function")
def create_pet():
    payload = {"id": 1,
               "name": "Nick",
               "status": "available"
               }
    response = requests.post(url=f"{BASE_URL}/pet", json=payload)
    assert response.status_code == 200
    return response.json()

@pytest.fixture
def create_order():
    order_id = 5
    order_url = f"{BASE_URL}/store/order/{order_id}"

    # Удаляем старый заказ, если он остался от прошлого запуска
    requests.delete(url=order_url)

    payload = {
        "id": order_id,
        "petId": 1,
        "quantity": 1,
        "status": "placed",
        "complete": True,
    }

    response = requests.post(
        url=f"{BASE_URL}/store/order",
        json=payload,
    )

    print("URL:", response.request.url)
    print("Тело запроса:", response.request.body)
    print("Статус:", response.status_code)
    print("Ответ:", response.text)

    assert response.status_code == 200, response.text

    yield response.json()

    # Удаляем заказ после выполнения теста
    requests.delete(url=order_url)