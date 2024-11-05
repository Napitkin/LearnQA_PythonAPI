import requests


def test_homework_header():
    response = requests.get("https://playground.learnqa.ru/api/homework_header")

    headers = response.headers

    for header, value in headers.items():
        print(f"Header name: {header}, Header value: {value}")

    # Проверяем, что в ответе содержится ожидаемый header с нужным значением
    assert "x-secret-homework-header" in headers, "Header 'x-secret-homework-header' не найден"
    assert headers["x-secret-homework-header"] == "Some secret value", "Неверное значение для 'x-secret-homework-header'"

