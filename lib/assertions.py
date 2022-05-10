import requests

# """СОЗДАЕМ КЛАСС Assertions"""
from requests import Response
import json  # для работы с json надо импортировать библиотеку json


class Assertions:
    # """СОЗДАЕМ МЕТОД, КОТОРЫЙ БУДЕТ ПРОВЕРЯТЬ, ЧТО ЗАПРОС ЯВЛЯЕТСЯ JSON И ТО ЧТО ИМЯ СОВПАДАЕТ С ОЖИДАЕМЫМ ИМЕНЕМ,
    # В СЛУЧАЕ ЕСЛИ ИМЯ НЕ СОВПАДЕТ С ОЖДАЕМЫМ РЕЗУЛЬТАТОМ, ПОЯВИТСЯ ОШИБКА"""
    @staticmethod
    def assert_json_value_by_name(response: Response, jsn_name, expected_value, error_message):
        # ПРИМЕНИМ КОНСТРУКЦИЮ try для проверки имени запроса в виде json
        try:
            response_as_dict = response.json()  # ПРЕВРАЩАЕТ ЗАПРОС JSON В СЛОВАРЬ {}
            # ЕСЛИ ФОРМАТ НЕ JSON ПАДАЕТ ОШИБКА
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format, response is {response.text}, {response.url}"
        # ЕСЛИ ФОРМАТ JSON ТО ИДЕТ СЛЕДУЮЩАЯ ПРОВЕРКА НА НАХОЖДЕНИЕ В ЗНАЧЕНИЕ В JSON, ЕСЛИ ЕГО НЕТ ПАДАЕТ ОШИБКА С ИСКОМЫМ ИМЕНЕМ
        # И С СОДЕРЖАНИЕМ JSON
        assert jsn_name in response_as_dict, f"Response JSON does not have key {jsn_name} {response_as_dict}"
        # ЕСЛИ ФОРМАТ ИМЯ СОДЕРЖИТСЯ ТО ПРОХОДИТ ПРОВЕРКА ОЖИДАЕМОГО И ФАКТИЧЕСКОГО ЗНАЧЕНИЕ, ЕСЛИ НЕ ПРОХОДИТ,
        # ТО ВОЗВРАЩАЕТ ОШИБКУ
        assert response_as_dict[jsn_name] == expected_value, error_message

    # """МЕТОД ПРОВЕРКИ ЗНАЧНЕИЯ В ПОЛЕ ПОХОЖ НА ПРЕДЫДУЩИЙ МЕТОД С JSON ТОЛЬКО ТУТ СООБЩЕНИЕ МЫ ЗАРАНЕЕ НЕ ЗНАЕМ
    # в методе используется только ЗАПРОС и имя"""
    @staticmethod
    def assert_json_has_key(response: Response, jsn_name):
        # ПРИМЕНИМ КОНСТРУКЦИЮ try для проверки имени запроса в виде json
        try:
            response_as_dict = response.json()  # ПРЕВРАЩАЕТ ЗАПРОС JSON В СЛОВАРЬ {}
            # ЕСЛИ ФОРМАТ НЕ JSON ПАДАЕТ ОШИБКА
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format, response is {response.text}, {response.url}"
        # ЕСЛИ ФОРМАТ JSON ТО ИДЕТ СЛЕДУЮЩАЯ ПРОВЕРКА НА НАХОЖДЕНИЕ В ЗНАЧЕНИЕ В JSON, ЕСЛИ ЕГО НЕТ ПАДАЕТ ОШИБКА С ИСКОМЫМ ИМЕНЕМ
        # И С СОДЕРЖАНИЕМ JSON
        assert jsn_name in response_as_dict, f"Response JSON does not have key {jsn_name} {response_as_dict}"
        # ЕСЛИ ФОРМАТ ИМЯ СОДЕРЖИТСЯ ТО ПРОХОДИТ ПРОВЕРКА ОЖИДАЕМОГО И ФАКТИЧЕСКОГО ЗНАЧЕНИЕ, ЕСЛИ НЕ ПРОХОДИТ,
        # ТО ВОЗВРАЩАЕТ ОШИБКУ
        # assert response_as_dict[jsn_name] == expected_value, error_message

    # """МЕТОД ПРОВЕРЯЕТ СООТВЕСТВУЕТ ЛИ КОД КОТОРЫЙ МЫ ХОТИМ ПОЛУЧИТЬ ФАКТИЧЕСКОМУ КОДУ, ЕСЛИ НЕ СООТВЕТСТВУЕТ,
    # ВЫДАЕТ ОШИБКУ"""
    # """Применим этот асерт в проверке на status_code в двух тестах test_created_user"""
    @staticmethod
    def asert_has_response_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, \
            f"Expected status_code {expected_status_code} not equal to {response.status_code}"

    # """МЕТОД ПРОВЕРЯЕТ НЕТУ ЛИ ЗАДАННОГО ПАРАМЕТРА В ФОРМАТЕ JSON В ОТВЕТЕ ОТ СЕРВЕРА"""

    @staticmethod
    def assert_json_has_no_key(response: Response, jsn_name):
        # ПРИМЕНИМ КОНСТРУКЦИЮ try для проверки имени запроса в виде json
        try:
            response_as_dict = response.json()  # ПРЕВРАЩАЕТ ЗАПРОС JSON В СЛОВАРЬ {}
            # ЕСЛИ ФОРМАТ НЕ JSON ПАДАЕТ ОШИБКА
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format, response is {response.text}, {response.url}"
        # ЕСЛИ ФОРМАТ JSON ТО ИДЕТ СЛЕДУЮЩАЯ ПРОВЕРКА НА НАХОЖДЕНИЕ В ЗНАЧЕНИЕ В JSON, ЕСЛИ ЕГО НЕТ ПАДАЕТ ОШИБКА С ИСКОМЫМ ИМЕНЕМ
        # И С СОДЕРЖАНИЕМ JSON
        assert jsn_name not in response_as_dict, f"Response should not have key {jsn_name} {response_as_dict}, but his present!"
        # ЕСЛИ ФОРМАТ ИМЯ не СОДЕРЖИТСЯ ТО ПРОХОДИТ ПРОВЕРКА ОЖИДАЕМОГО И ФАКТИЧЕСКОГО ЗНАЧЕНИЕ, ЕСЛИ ПРОХОДИТ,
        # ТО ВОЗВРАЩАЕТ ОШИБКУ
        # assert response_as_dict[jsn_name] == expected_value, error_message

    # """ДАННЫЙ МЕТОД ПРОВЕРЯЕТ НАЛИЧИЕ КЛЮЧЕЙ В JSON ОТВЕТЕ В СООТВЕСТВИИ С ВВЕДЕННЫМИ ЗНАЧЕНИЯМИ"""
    @staticmethod
    def assert_json_has_more_then_one_keys(response: Response, jsn_names: list):
        # ПРИМЕНИМ КОНСТРУКЦИЮ try для проверки имени запроса в виде json
        try:
            response_as_dict = response.json()  # ПРЕВРАЩАЕТ ЗАПРОС JSON В СЛОВАРЬ {}
            # ЕСЛИ ФОРМАТ НЕ JSON ПАДАЕТ ОШИБКА
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format, response is {response.text}, {response.url}"
        # ЕСЛИ ФОРМАТ JSON ТО ИДЕТ СЛЕДУЮЩАЯ ПРОВЕРКА НА НАХОЖДЕНИЕ В ЗНАЧЕНИЕ В JSON, ЕСЛИ ЕГО НЕТ ПАДАЕТ ОШИБКА С ИСКОМЫМ ИМЕНЕМ
        # И С СОДЕРЖАНИЕМ JSON

        # """ДЛЯ ТОГО ЧТОБЫ ПРОВЕРЯТЬ СПИСОК ИЗ ЗНАЧЕНИЙ НУЖНО ДОБАВИТЬ ЦИКЛ КОТОРЫЙ БУДЕТ ИДТИ ПО СПИСКУ И СРАВНИВАТЬ В АССЕРТЕ """
        for jsn_name in jsn_names:
            assert jsn_name in response_as_dict, f"Response JSON does not have key {jsn_name} {response_as_dict}"
        # ЕСЛИ ФОРМАТ ИМЯ СОДЕРЖИТСЯ ТО ПРОХОДИТ ПРОВЕРКА ОЖИДАЕМОГО И ФАКТИЧЕСКОГО ЗНАЧЕНИЕ, ЕСЛИ НЕ ПРОХОДИТ,
        # ТО ВОЗВРАЩАЕТ ОШИБКУ
        # assert response_as_dict[jsn_name] == expected_value, error_message

    # """МЕТОД ПОЗВОЛЯЕТ ПРОВЕРИТЬ НЕСКОЛЬКО КЛЮЧЕЙ НА ОТСУТСТВИЕ В JSON"""
    @staticmethod
    def assert_json_has_no_any_keys(response: Response, jsn_names: list):
        # ПРИМЕНИМ КОНСТРУКЦИЮ try для проверки имени запроса в виде json
        try:
            response_as_dict = response.json()  # ПРЕВРАЩАЕТ ЗАПРОС JSON В СЛОВАРЬ {}
            # ЕСЛИ ФОРМАТ НЕ JSON ПАДАЕТ ОШИБКА
        except json.JSONDecodeError:
            assert False, f"Response is not JSON format, response is {response.text}, {response.url}"
        # ЕСЛИ ФОРМАТ JSON ТО ИДЕТ СЛЕДУЮЩАЯ ПРОВЕРКА НА НАХОЖДЕНИЕ В ЗНАЧЕНИЕ В JSON, ЕСЛИ ЕГО НЕТ ПАДАЕТ ОШИБКА С ИСКОМЫМ ИМЕНЕМ
        # И С СОДЕРЖАНИЕМ JSON
        for jsn_name in jsn_names:
            assert jsn_name not in response_as_dict, f"Response should not have key {jsn_name} {response_as_dict}, but his present!"
        # ЕСЛИ ФОРМАТ ИМЯ не СОДЕРЖИТСЯ ТО ПРОХОДИТ ПРОВЕРКА ОЖИДАЕМОГО И ФАКТИЧЕСКОГО ЗНАЧЕНИЕ, ЕСЛИ ПРОХОДИТ,
        # ТО ВОЗВРАЩАЕТ ОШИБКУ
        # assert response_as_dict[jsn_name] == expected_value, error_message
