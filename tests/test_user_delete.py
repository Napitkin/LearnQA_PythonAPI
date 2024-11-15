import time
import allure

from LearnQA_Python_API.lib.base_case import BaseCase
from LearnQA_Python_API.lib.assertions import Assertions
from LearnQA_Python_API.lib.my_requests import MyRequests


@allure.epic("User Management")
@allure.feature("User Deletion")
class TestUserDelete(BaseCase):

    @allure.description("Удаление пользователя с ID=2")
    def test_delete_user_with_id_2(self):
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }

        # Авторизация
        response1 = MyRequests.post("/user/login", data=data)

        Assertions.assert_code_status(response1, 200)  # Проверка успешной авторизации
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        # Попытка удалить пользователя с ID 2
        response2 = MyRequests.delete(
            "/user/2",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == '{"error":"Please, do not delete test users with ID 1, 2, 3, 4 or 5."}', \
            "Unexpected response when trying to delete user with ID 2"


    @allure.description("Создание пользователя, авторизоваться под ним и удалить. Затем получить его данные под ID")
    def test_delete_just_created_user(self):
        # Регистрация нового пользователя
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")
        email = register_data["email"]
        password = register_data["password"]

        # Авторизация под созданным пользователем
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        Assertions.assert_code_status(response2, 200)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # Удаление созданного пользователя
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response3, 200)

        # Попытка получить данные удалённого пользователя
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf-8") == "User not found", "Unexpected response content for deleted user"


    @allure.description("Попытка удалить пользователя, авторизовавшись под другим пользователем")
    def test_delete_user_authorized_as_another_user(self):
        # Регистрация двух пользователей
        # Создание первого пользователя
        register_data1 = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data1)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id1 = self.get_json_value(response1, "id")
        time.sleep(1)

        # Создание второго пользователя
        register_data2 = self.prepare_registration_data()
        response2 = MyRequests.post("/user/", data=register_data2)

        Assertions.assert_code_status(response2, 200)
        Assertions.assert_json_has_key(response2, "id")

        email2 = register_data2["email"]
        password2 = register_data2["password"]
        time.sleep(1)

        # Авторизация под вторым пользователем
        login_data_2= {
            "email": email2,
            "password": password2
        }
        response3 = MyRequests.post("/user/login", data=login_data_2)

        Assertions.assert_code_status(response3, 200)
        auth_sid = self.get_cookie(response3, "auth_sid")
        token = self.get_header(response3, "x-csrf-token")
        time.sleep(2)

        # Попытка удалить первого пользователя, будучи авторизованным под вторым
        response4 = MyRequests.delete(
            f"/user/{user_id1}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_code_status(response4, 400)  # Тут похоже баг, т.к. пользователь удаляется! Пробовал через Postman отправлять запросы
        # на регистрацию 2-х пользователей, авторизацию вторым пользователем и попыткой удалить первого пользователя, так же приходит ответ сервера 200.
