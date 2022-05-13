# """СОЗДАЕМ В ПАПКЕ lib файл my_requests"""
# """В НЕМ МЫ СОЗДАДИМ КЛАСС MyRequests""
import requests
import allure

from lib.loger import Logger


class MyRequests:
    # """МЕТОД НАЧИНАЕТСЯ С НИЖНЕГО ПОДЧЕРКИВАНЬЯ И ЯВЛЯЕТСЯ ПРИВАТНЫМ В НЕГО ПЕРЕДАЕМ
    # все то что мы передаем в запросе
    # url - ссылка на ресурс,
    # data - это данные для PUT и POST запросов,
    # headers - для GET запросов,
    # cookies - наприме для авторизации,
    # method
    # """

    @staticmethod #МЕТОД возвращает и send полученные данные с методом POST
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"POST request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, 'POST')


    @staticmethod #МЕТОД возвращает и send полученные данные с методом PUT
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"PUT request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, 'PUT')

    @staticmethod #МЕТОД возвращает и send полученные данные с методом GET
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"GET request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, 'GET')

    @staticmethod #МЕТОД возвращает и send полученные данные с методом DELETE
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        with allure.step(f"DELETE request to URL '{url}'"):
            return MyRequests._send(url, data, headers, cookies, 'DELETE')

    @staticmethod
    def _send(url:str, data:dict, headers:dict, cookies:dict, method:str):
        # ЗДЕСЬ МЫ ОДИН РАЗ НАПИШЕМ ДОМЕН НАШЕГО API
        # в запросе будем писать только URI
        url = f"https://playground.learnqa.ru/api{url}"

        # """
        # ВНУТРИ МЕТОДА СОЗДАДИМ ПРОВЕРКУ
        #  которая позволит заполнить cookies и headers пустым масивом,
        #  если их не введут в запросе
        #  """
        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        # """ПОСЛЕ ИФОВ ПИШЕМ ДЛЯ ЛОГГЕРА ДАННЫЕ"""
        # """ЛОГГЕР ПОЛУЧАЕТ ИНФОРМАЦЮ ОТ ПОЛЬЗОВВАТЕЛЯ, какой запрос он делает"""
        Logger.add_request(url, data, headers, cookies, method)
        # """
        # # ДАЛЕЕ НАПИШЕМ КОД ДЛЯ ВЫБОРА МЕТОДА КОТОРЫМ БУДЕТ ЗАПУЩЕН ТЕСТ
        # ЭТИМ МЕТОДЫ ЯВЛЯЮТСЯ ПРИВАТНЫМИ ПОЭТОМУ ИХ НУЖНА ПЕРЕДАТЬ В STAICKMETHODS
        # """
        #если method GET - передается параметры для get запроса
        if method == "GET":
            response = requests.get(url, params=data, headers=headers, cookies=cookies)

        #ЕСЛИ МЕТОД POST ПЕРЕДАЮТСЯ ПАРАМЕТРЫ ДЛЯ POST ЗАПРОСА
        elif method == "POST":
            response = requests.post(url, data=data, headers=headers, cookies=cookies)

        # ЕСЛИ МЕТОД PUT ПЕРЕДАЮТСЯ ПАРАМЕТРЫ ДЛЯ PUT ЗАПРОСА
        elif method == "PUT":
            response = requests.put(url, data=data, headers=headers, cookies=cookies)

        # ЕСЛИ МЕТОД DELETE ПЕРЕДАЮТСЯ ПАРАМЕТРЫ ДЛЯ DELETE ЗАПРОСА
        elif method == "DELETE":
            response = requests.delete(url, data=data, headers=headers, cookies=cookies)

        else:
            raise Exception(f"Bad HTTP method '{method}' was recived")

        # """ЗДЕСЬ ЛОГГЕР ПОЛУЧАЕТ ЗАПРОС КОТОРЫЙ ПОЛЬЗОВАТЕЛЬ ДЕЛАЕТ"""

        Logger.add_response(response)

        return response






