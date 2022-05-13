import json.decoder
from datetime import datetime


import requests

# """ВНАЧАЕ ЗАПИШЕМ В КЛАСС МЕТОДЫ ДЛЯ ПОЛУЧЕНИЯ ЗНАЧЕНИЙ КУКИ И ХЭДЭР ИЗ ОТВЕТА СЕРВЕРА ПО ИМЕНИ
# СУТЬ ИХ В СЛЕДУЮЩЕМ СНАЧАЛА ПЕРЕДАЕМ ОБЪЕКТ ОТВЕТА КОТОРОЕ МЫ ПОЛУЧАЕМ ПОСЛЕ ЗАПРОСА И ИМЯ ИЗ КОТОРОГО
# ПО ЭТОМУ ОТВЕТУ МЫ БУДЕМ ПОЛУЧАТЬ ЛИБО ХЭДЭР ЛИБО КУКИ,  МЕТОД БУДЕТ ПОНИМАТЬ ЕСТЬ ЛИ ТАКИЕ ДАННЫЕ В ОТВЕТЕ, ЕСЛИ ИХ НЕТ
# ТЕСТ  БУДЕТ ПАДАТЬ, ЕСЛИ ОНИ ЕСТЬ БУДЕТ ИХ ВОЗВРАЩАТЬ
# """
from requests import Response

from lib.loger import Logger


class BaseCase:
    # Метод получает ответ от сервера и сопоставляет его с именем куки, которое мы введем в других тестах
    def get_cookie(self, response: Response, cookies_name):
        # ВНУТРИ ФУНКЦИИ ПИШЕМ ASSERT ОН ПРОВЕРЯЕТ ЕСТЬ ЛИ ИМЯ ВНУТРИ КУКИ В ЗАПРОСЕ КОТОРЫЙ МЫ ОТПРАВЛЯЕМ И ХОТИМ ПОЛУЧИТЬ
        assert cookies_name in response.cookies, f"Cannot find {cookies_name} in {response.text} {response.cookies}"
        return response.cookies[cookies_name]  # если проверка проходим нам возвращается искомое значение из куки

    # ДЕЛАЕМ ТАКОЙ ЖЕ МЕТОД ДЛЯ ПОЛУЧЕНИЯ ИНФОРМАЦИИ ИЗ ХЭДЕРА
    def get_header(self, response: Response, headers_name):
        # ВНУТРИ ФУНКЦИИ ВЫЗЫВАЕМ АССЕРТ КОТОРЫЙ ПРОВЕРИТ ЕСЛИ ТАКОЕ ИМЯ В ХЭДЕРЕ, ЕСЛИ ЕГО НЕ БУДЕТ
        # ТЕСТ УПАДЕТ С ОШИБКОЙ
        assert headers_name in response.headers, f"Cannot find {headers_name} in {response.text} {response.headers}"
        return response.headers[headers_name]  # ЕСЛИ ТАКОЕ ИМЯ ЕСТЬ, ФУНКИЯ ВЕРНЕТ ЕГО НАМ

    # """ПРИМЕНИМ ЭТИ МЕТОДЫ ВНУТРИ ФАЙЛАЙ test_for_base_case.py"""
    # get_cookie() применяется в:
    # auth_sid

    # get_header() применяется:
    # auth_x_csrf_token

    # """ДОБАВИМ В BaseCase еще одну функцию для работы с JSON"""
    # ФУНКЦИЯ ПРИНИМАЕТ ЗАПРОС, И ПРОВЕРЯЕТ ЕГО НА НАЛИЧИЕ ИМЕНИ, ЕСЛИ ИМЯ ЕСТЬ ВОЗВРАЩАЕТ ЕГО

    def get_json_value(self, response: Response, json_name):
        # #МЕТОД ОБОРАЧИВАЕТСЯ В TRY, EXCEPT ДЛЯ ТОГО, ЧТОБЫ ПРОВЕРИТЬ ЯВЛЯЕТСЯ ЛИ ПОЛУЧЕННАЯ ИНФОРМАЦИЯ ОТ СЕРВЕРА
        # JSON И ЕСЛИ ЯВЯЛЕТСЯ, ТО ВОЗРАЩАЕТ ИСКОМОЕ ИМЯ, А ЕСЛИ НЕ ЯВЯЛЕТСЯ, ПАДАЕТ С ОШИБКОЙ
        try:
            response_as_dict = response.json()  # превращаем JSON ФАЙЛ В ФОРМАТ СЛОВАРЯ {}
        except json.decoder.JSONDecodeError:
            # помощью этой проверки мы убеждаемся, что формат JSON иначе падает с ошибкой
            # нужно импортировать json.decoder.JSONDecodeError
            assert False, f"Response is no JSON format, response is formt {response.text}"

        # ЕСЛИ ЗАПРОС ПРОХОДИТ ПРОВЕРКУ НА JSON ФОРМАТ, ТО ДЕЛАЕТСЯ СЛЕДУЮЩАЯ ПРОВЕРКА
        # ЕСЛИ ИМЯ СОДЕРЖАТЬ В СПИСКЕ JSON ТО ВОЗВРАЩЕТСЯ ИМЯ, ЕСЛИ НЕТ, ПАДАЕТ ОШИБКА
        assert json_name in response_as_dict, f"Response does not contain json_name {json_name} in {response.text}"
        # ЕСЛИ ПРОВЕРКА ПРОХОДИТ
        return response_as_dict[json_name]

    def prepare_registration_data(self, email=None):

        if email is None:
            base_part = "learnqa"
            domain = "example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}@{domain}"

        return {
            "password": "123",
            "username": 'learnqa',
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email
        }
