import allure
import pytest
import requests
import jsonschema
from tests.shemas.pet_shemas import PET_SCHEMA


BASE_URL = "https://petstore3.swagger.io/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса кода ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожиданием"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {"id": 9999,
                       "name": "Non-existent Pet",
                       "status": "available"
                      }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса кода ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожиданием"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"


    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                       "id": 1,
                       "name": "Nick",
                       "status": "available"
                      }

        with allure.step("Отправка запроса на создания питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа и валидации JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json()['id'] == payload ['id'], 'id питомца не совпадает с ожидаемым'
            assert response.json()['name'] == payload['name'], 'name питомца не совпадает с ожидаемым'
            assert response.json()['status'] == payload['status'], 'status питомца не совпадает с ожидаемым'

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self,create_pet):
        with allure.step("Получение ID созданного питомца"):
           pet_id = create_pet["id"]
        with allure.step("Отрпавка запроса на получение информации о питомце по ID"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()['id'] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_update_pet_by_id(self,create_pet):
        with allure.step("Получение ID созданного питомца"):
           pet_id = create_pet["id"]
        with allure.step("Получение данных для обновления"):
            pet_for_update = {
                "id": 1,
                "name": "Barry",
                "status": "Sold"
            }
        with allure.step("Отправка запроса на обновление информации о питомце по ID"):
            response = requests.put(url=f"{BASE_URL}/pet", json=pet_for_update)

        with allure.step("Проверка статуса ответа и обновление данных питомца"):
            assert response.status_code == 200
            response_json = response.json()
            assert response_json["id"] == pet_for_update["id"]
            assert response_json["name"] == pet_for_update["name"]
            assert response_json["status"] == pet_for_update["status"]

    @allure.title("Удаление питомца")
    def test_delete_pet_by_id(self,create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]
        with allure.step("Удаление питомца по ID"):
            requests.delete(url=f"{BASE_URL}/pet/{pet_id}")
        with allure.step("Отправка запроса GET по ID питомца"):
            response = requests.get(url=f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404

    @allure.title("Получение списка питомцев по статусу")
    @pytest.mark.parametrize(
        "status, expected_status_code",
        [

            ("available", 200),
            ("pending", 200),
            ("sold",200),
            ("  ",400)
        ]
    )
    def test_get_pet_by_status(self, status, expected_status_code):
        with allure.step(f"Отправка запроса на получение питомцев по статусу {status}"):
            response = requests.get(url=f"{BASE_URL}/pet/findByStatus",params={"status": status})
            assert response.status_code == expected_status_code
            if expected_status_code == 200:
                assert isinstance(response.json(), list)
            elif expected_status_code == 400:
                try:
                    assert isinstance(response.json(), dict)
                except requests.exceptions.JSONDecodeError:
                    assert isinstance(response.text, str)


    @allure.title("Размещение заказа")
    def test_create_order(self):
        with allure.step(f"Отравка запроса на создание заказа"):
            payload = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
            response = requests.post(url=f"{BASE_URL}/store/order", json=payload)
            if response.status_code == 200:
                assert response.json() == payload
            elif response.status_code == 500:
                error_data = response.json()

                assert error_data["code"] == 500
                assert "message" in error_data

    @allure.title("Получение информации о заказе по ID")
    def test_get_information_by_id(self):
        with allure.step("Отправка запроса на получение информации по ID"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
            if  response.status_code == 200:
                assert response.json()["id"] == 1
            elif response.status_code == 500:
                error_data = response.json()
                assert error_data["code"] == 500
                assert "message" in error_data

    @allure.title("Удаление заказа по ID")
    def test_delete_order_by_id(self):
        with allure.step("Отправка запроса на удаление заказа по ID"):
            delete_response = requests.delete(url=f"{BASE_URL}/store/order/1")
            assert delete_response.status_code == 200
        with allure.step("Проверка на отсутствие заказа при отправке запроса"):
            response = requests.get(url=f"{BASE_URL}/store/order/1")
            assert response.status_code == 404


    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_order_nonexistent_info(self,create_order):
        order_id = create_order["id"]
        delete_response = requests.delete(url=f"{BASE_URL}/store/order/{order_id}")
        assert delete_response.status_code == 200

        with allure.step("Отправка запроса на получение информации о несуществующем заказе"):
            response = requests.get(url=f"{BASE_URL}/store/order/{order_id}")
            assert response.status_code == 404
            error_data = response.json()
            assert isinstance(error_data, dict)



