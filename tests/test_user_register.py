import allure
import pytest
from LearnQA_Python_API.lib.base_case import BaseCase
from LearnQA_Python_API.lib.assertions import Assertions
from LearnQA_Python_API.lib.my_requests import MyRequests


@allure.epic("User Management")
@allure.feature("User Information")
class TestUserRegister(BaseCase):

    @allure.description("Успешное создание пользователя")
    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 200)
        Assertions.assert_json_has_key(response, "id")


    @allure.description("Создание пользователя с существующей почтой")
    def test_create_user_with_existing_email(self):
        email = "vinkotov@example.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response.content}"


    @allure.description("Создание пользователя с некорректной почтой")
    def test_create_user_with_invalid_email(self):
        email = "vinkotovexample.com"
        data = self.prepare_registration_data(email)

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "Invalid email format", f"Unexpected response content {response.content}"


    @pytest.mark.parametrize("delete_field", ["password", "username", "firstName", "lastName", "email"])
    @allure.description("Создание пользователя без одного обязательного поля")
    def test_create_user_without_mandatory_field(self, delete_field):
        data = self.prepare_registration_data()
        data.pop(delete_field)  # Удаление одного обязательного поля

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == f"The following required params are missed: {delete_field}", f"Unexpected response content {response.content}"


    @allure.description("С коротким именем в 1 символ")
    def test_create_user_with_short_username(self):
        data = self.prepare_registration_data()
        data["username"] = "a"  # Создание пользователя с очень коротким именем в один символ

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too short", f"Unexpected response content {response.content}"


    @allure.description("Создание пользователя с очень длинным именем")
    def test_create_user_with_long_username(self):
        data = self.prepare_registration_data()
        data["username"] = "a" * 251  # Создание пользователя с очень длинным именем - длиннее 250 символов

        response = MyRequests.post("/user/", data=data)

        Assertions.assert_code_status(response, 400)
        assert response.content.decode("utf-8") == "The value of 'username' field is too long", f"Unexpected response content {response.content}"
