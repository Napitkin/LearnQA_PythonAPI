import requests

url = "https://playground.learnqa.ru/ajax/api/compare_query_type"
methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD']

#1. Делаем http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.
response_1 = requests.get(url, params={"": "GET"})
print("Ответ на задание 1 :" + response_1.text) # Возвращается ответ сервера: "Wrong method provided"

# 2. Делаем http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.
response_2 = requests.head(url, data={"method": "HEAD"})
print("Ответ на задание 2 :" + response_2.text) # Возвращается пустой ответ сервера

# 3. Делаем запрос с правильным значением method. Описать что будет выводиться в этом случае.
response_3 = requests.get(url, params={"method": "GET"})
print("Ответ на задание 3 :" + response_3.text) # Возвращается корректный ответ сервера: {"success":"!"}

# 4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method.
# Например с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
# И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра, но сервер отвечает так,
# словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так.

# Цикл для проверки всех сочетаний:
for real_method in methods:
    for param_method in methods:
        params = {'method': param_method}
        if real_method == 'GET':
            response = requests.get(url, params=params)
        elif real_method == 'POST':
            response = requests.post(url, data=params)
        elif real_method == 'PUT':
            response = requests.put(url, data=params)
        elif real_method == 'DELETE':
            response = requests.delete(url, data=params)
        elif real_method == 'HEAD':
            response = requests.head(url, data=params)
        print(f"Отправляемый метод: {real_method}, Сравневыемый метод: {param_method}, Результат: {response.text}")
# Реальный метод DELETE при сравнении с методом GET даёт ложное сообщение о корректном отправленном запросе: {"success":"!"}