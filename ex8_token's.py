import requests
import time

# Шаг 1: Создаем задачу
response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job").json()

# Извлекаем значения из ответа
seconds = response['seconds']
token = response['token']

print(f"Задача создана. Задача будет выполнена через {seconds} секунд. Токен: {token}")

# Шаг 2: Проверяем статус задачи до завершения
status_response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token}).json()

print(f"Статус задачи перед ожиданием: {status_response['status']}")  # Ожидаем, что статус будет "Job is NOT ready"

# Шаг 3: Ждем нужное количество секунд
time.sleep(seconds)

# Шаг 4: Проверяем статус задачи после завершения
status_response = requests.get("https://playground.learnqa.ru/ajax/api/longtime_job", params={"token": token}).json()

print(f"Статус задачи после ожидания: {status_response['status']}")  # Ожидаем, что статус будет "Job is ready"
if 'result' in status_response:
    print(f"Результат выполнения задачи: {status_response['result']}")
else:
    print("Результат еще не готов.")
