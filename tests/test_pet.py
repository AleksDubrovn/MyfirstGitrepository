import allure
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
            response_json = response.json()
            
        with allure.step("Проверка параметров питомца в ответе"):
            assert response.json()['id'] == payload ['id'], 'id питомца не совпадает с ожидаемым'
            assert response.json()['name'] == payload['name'], 'name питомца не совпадает с ожидаемым'
            assert response.json()['status'] == payload['status'], 'status питомца не совпадает с ожидаемым'