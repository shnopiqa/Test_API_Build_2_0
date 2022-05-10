from datetime import datetime

import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests  # импортируем my_requests из либ


# """"КЛАСС ДЛЯ ТЕСТИРОВАНИЕЯ РЕГИСТРАЦИИ ПОЛЬЗОВАТЕЛЯ"""
# ИМПОРТИРУЕМ РЕКВЕСТ, BaseCase from lib
# import Assertions


class TestUserRegister(BaseCase):

    # """МЕТОД Setup будет рандомно генерировать эмэйлы через библиотеку datetime"""
    def setup(self):
        base_part = "learnqa"  # БАЗОВАЯ ЧАСТЬ НАШЕГО ЭМЙЛА, ТО С ЧЕГО БУДЕТ НАЧИНАЕТЬСЯ НАШ ЭМЭЙЛ
        domain = "example.com"  # ПОТОМ ИДЕТ ДОМЕН example.com
        random_part = datetime.now().strftime("%m%d%Y%H%M%S")  # Генерируемая часть эмэйла, для его уникализации
        self.email = f"{base_part}{random_part}@{domain}"  # конструктор которы превращает эмэйл в уникальный

    # '''ПЕРВЫЙ ТЕСТ - ПОЗИТИВНЫЙ ТЕСТ НА РЕГИСТРАЦИЮ '''

    def test_create_user_successfully(self):
        data = {

            "password": "1234",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": self.email  # УНИКАЛЬНЫЙ ЭМЭЙЛ СГЕНИРИРОВАННЫЙ В СИСТЕМЕ
        }

        # #метод нужен для создания нового пользователя
        response2 = MyRequests.post("/user/",
                                    data=data)  # Response с применением MyRequests,

        # """ДОБАВИМ В assertions/lib метод для проверки поля id после регистрации"""
        # assert response2.status_code == 200, f"Unexpected status code {response2.status_code}, {response2.url}"
        # """Заменим проверку на статус код методом из assertions"""
        Assertions.asert_has_response_code(response2, 200) # МЕТОД ПРОВЕРЯЕТ, ЧТО СТАТУС КОД ЗАПРОСА СООТВЕТСВУТЕ ОЖИДАЕМОМУ
        # ЭТОТ МЕТОД БЕРЕТ В СЕБЯ ЗАПРОС И КЛЮЧ КОТОРЫЙ МЫ ХОТИМ НАЙТИ
        # И В СЛУЧАЕ ЕСЛИ НЕ НАХОДИТ, ВЫДАЕТ ОШИБКУ .
        Assertions.assert_json_has_key(response2, "id")
        # print(response2.content)

    # '''ВТОРОЙ ТЕСТ БУДЕТ НЕГАТИВНЫМ МЕТОД БУДЕТ ПРОВЕРЯТЬ РЕГИСТРАЦИЮ С СУЩЕСТВУЮЩИМ ЭМЭЙЛОМ'''
    def test_create_user_with_exiting_email(self):
        # ДАННЫЕ ДЛЯ РЕГИСТРАЦИИ
        # ВЫНЕСЕМ email из data в начало метода
        email = "vinkotov@example.com"
        data = {

            "password": "1234",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email  # ВВЕДЕН ЭМЭЙЛ, КОТОРЫЙ УЖЕ ЗАРЕГИСТРИРОВАН В СИСТЕМЕ
        }

        # #метод нужен для создания нового пользователя
        response1 = MyRequests.post("/user/",
                                    data=data)  # Response с применением MyRequests,

        # assert response1.status_code == 400, f"Unexpected status code: {response1.status_code}, {response1.content}"  # ПРОВЕРКА НА СТАТУС КОД
        # """Заменим проверку на статус код методом из assertions"""
        Assertions.asert_has_response_code(response1, 400) # # МЕТОД ПРОВЕРЯЕТ, ЧТО СТАТУС КОД ЗАПРОСА СООТВЕТСВУТЕ ОЖИДАЕМОМУ
        # ПРИВОДИМ КОНТЕНТ К UTF-8 разметке
        assert response1.content.decode(
            "utf-8") == f"Users with email '{email}' already exists", f"Unexpected response content {response1.status_code}, {response1.content}"  # ПРОВЕРКА НА КОТЕНТ
        # print(response1.status_code)  # ПЕЧАТАЕТ СТАТУС КОД ОТ СЕРВЕРА НУЖНО ЧТОБЫ ПОСМОТРЕТЬ КАКОЙ КОД И КАКОЕ СООББЩЕНИЕ
        # print(response1.content)  # ПЕЧАТАЕТ КОНТЕНТ - ОТВЕТ ОТ СЕРВЕРА
