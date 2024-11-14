from LearnQA_Python_API.lib.base_case import BaseCase
from LearnQA_Python_API.lib.assertions import Assertions
from LearnQA_Python_API.lib.my_requests import MyRequests


class TestUserEdit(BaseCase):
    def test_user_edit_just_created_user(self):
        # REGISTER
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data["email"]
        first_name = register_data["firstName"]
        password = register_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        # EDIT
        new_name = "Changed Name"
        response3 = MyRequests.put(f"/user/{user_id}",
                    headers={"x-csrf-token": token},
                    cookies={"auth_sid": auth_sid},
                    data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)

        # EDIT#1 Попытаемся изменить данные пользователя, будучи неавторизованными
        new_name = "Changed Name"
        response4 = MyRequests.put(f"/user/2", data={"firstName": new_name})

        Assertions.assert_code_status(response4, 400)
        assert response4.content.decode("utf-8") == '{"error":"Auth token not supplied"}', 'Unexpected response content when editing without auth'

        # EDIT#2 Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
        data = {
            "email": "vinkotov@example.com",
            "password": "1234"
        }
        response5 = MyRequests.post("/user/login", data=data)

        auth_sid_e2  = self.get_cookie(response5, "auth_sid")
        token_e2  = self.get_header(response5, "x-csrf-token")
        #Попытка изменить другого пользователя
        new_name_e2 = "Random Name"
        response6 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": auth_sid_e2 },
            cookies={"auth_sid": token_e2},
            data={"firstName": new_name_e2}
        )

        Assertions.assert_code_status(response6, 400)
        assert response6.content.decode("utf-8") == '{"error":"Auth token not supplied"}', 'Unexpected response when editing as another user'

        # EDIT#3 Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @
        response7 = MyRequests.post("/user/login", data=login_data)

        auth_sid_e3 = self.get_cookie(response7, "auth_sid")
        token_e3 = self.get_header(response7, "x-csrf-token")
        user_id_e3 = self.get_json_value(response7, "user_id")

        # Попытка изменить email на неверный формат
        new_email = "newemailvinkotovexample.com"  # отсутствует символ @
        response8 = MyRequests.put(
            f"/user/{user_id_e3}",
            headers={"x-csrf-token": token_e3},
            cookies={"auth_sid": auth_sid_e3},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response8, 400)
        assert response8.content.decode("utf-8") == '{"error":"Invalid email format"}', 'Unexpected response for invalid email format'

        # EDIT#4 Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
        response9 = MyRequests.post("/user/login", data=login_data)

        auth_sid_e4 = self.get_cookie(response9, "auth_sid")
        token_e4 = self.get_header(response9, "x-csrf-token")
        user_id_e4 = self.get_json_value(response9, "user_id")

        # Попытка изменить firstName на слишком короткое значение
        new_firstname = "k"  # всего один символ
        response10 = MyRequests.put(
            f"/user/{user_id_e4}",
            headers={"x-csrf-token": token_e4},
            cookies={"auth_sid": auth_sid_e4},
            data={"firstName": new_firstname}
        )

        Assertions.assert_code_status(response10, 400)
        assert response10.content.decode("utf-8") == '{"error":"The value for field `firstName` is too short"}', 'Unexpected response for too short firstName'

        # GET
        response11 = MyRequests.get(
            f"/user/{user_id}",
                headers={"x-csrf-token": token},
                cookies={"auth_sid": auth_sid})

        Assertions.assert_json_value_by_name(response11, "firstName", new_name, "Wrong name of the user after edit")