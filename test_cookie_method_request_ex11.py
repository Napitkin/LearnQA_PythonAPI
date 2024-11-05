import requests


def test_homework_cookie():
    response = requests.get("https://playground.learnqa.ru/api/homework_cookie")

    cookies = response.cookies

    for cookie in cookies:
        print(f"Cookie name: {cookie.name}, Cookie value: {cookie.value}")

    # Проверяем, что в ответе содержится ожидаемая cookie с нужным значением
    assert "HomeWork" in cookies, "Cookie 'HomeWork' не найдена"
    assert cookies["HomeWork"] == "hw_value", "Неверное значение для 'HomeWork' cookie"
