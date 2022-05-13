import datetime

# """Создадим класс для логирования файлов"""
# """создадим папку лог в корневой директории"""
import os

from requests import Response


class Logger:
    # """добавим переменную для генерации имени лога"""
    file_name = f"logs/log_" + str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + ".log"

    # """НАПИШЕМ ФУНКЦИЮ КОТОРАЯ ПИШЕТ В ЭТОТ ФАЙЛ ДАННЫЕ ИЗ ТЕСТОВ"
    # ФУНКЦИЯ С КЛАССМЕТОДОМ, В НЕЕ ПОПАДАЮТ ДАННЫЕ В ВИДЕ СТРОКИ
    # ФУНКЦИЯ ЗАПИСЫВАЕТ ДАННЫЕ КОТОРЫЕ ПРИХОДЯТ В ПЕРЕМЕННУЮ data и делает из них файл с логами""
    @classmethod
    def _write_log_to_file(cls, data: str):
        with open(cls.file_name, "a", encoding="utf-8") as logger_file:
            logger_file.write(data)

    # """МЕТОД ПОЛУЧАЕТ ДАННЫЕ ИЗ ТЕСТОВ И ПЕРЕДАЕТ ИХ В ФУНКЦИЮ КОТОРАЯ ЗАПИСЫВАЕТ ЛОГИ, НА ВХОД ПОЛУЧАЕТ
    # URL, COOKIE, DATA, HEADERS, METHODS И ВСЕ ЭТО БУДЕМ ПРЕВРАЩАТЬ В СТРОКУ"""
    @classmethod
    def add_request(cls, url: str, data: dict, headers: dict, cookies: dict, method: str):
        # В ЭТУ ПЕРЕМЕННУЮ ЗАПИСЫВАЕТ ИМЯ ДЛЯ ТЕСТОВ? С ПОМОЩЬЮ НЕЕ ПАЙТЕСТ ГОВОРИТ КАКОЙ ТЕСТ СЕЙЧАС ЗАПУЩЕН
        # И КАК ОН НАЗЫВАЕТСЯ
        testname = os.environ.get("PYTEST_CURRENT_TEST")

        # """МЕТОД ПЕРЕВОДЯЩИМЙ ДАННЫЕ ИЗ ТЕСТОВ В СТРОКУ"""
        data_to_add = f"\n----\n"
        data_to_add += f"Test: {testname}\n"  # В лог записывается название теста
        data_to_add += f"Time: {str(datetime.datetime.now())}\n"  # ОТОБРАЖАЕТ ВРЕМЯ В КОТОРОЕ ПРОИСХОДИТ ПРОВЕРКА
        data_to_add += f"Request URL: {url}\n"
        data_to_add += f"Request data: {data}\n" # ЛОГИН И ПАРОЛЬ КОТОРЫЙ ВВОДИТСЯ
        data_to_add += f"Request method: {method}\n"  # в строку переводится методе
        data_to_add += f"Request headers: {headers}\n"  # headers
        data_to_add += f"Request cookies: {cookies}\n"
        data_to_add += "\n"
        #
        # """ЗАПИШЕМ ПОДГОТОВЛЕННЫЕ ДАННЫЕ ПРЕВРАЩЕННЫЕ В СТРОКУ В ФАЙЛ"""

        cls._write_log_to_file(data_to_add)  # В файл записываются данные

        # """НАПИШЕМ МЕТОД ДЛЯ ЗАПИСИ ОТВЕТА СЕРВЕРА
        # ПРИНИМАЕТ ОТВЕТЫ ОТ СЕРВЕР И ЛОГГИРУЕТ ИХ"""

    @classmethod
    def add_response(cls, response: Response):
        cookies_as_dict = dict(response.cookies)  # ЗАПИСЫВАЮТСЯ КУКИ В ПЕРЕМЕННУЮ ОТ СЕРВЕРА
        headers_as_dict = dict(response.headers)  # ЗАПИСЫВАЮТСЯ header В ПЕРЕМЕННУЮ ОТ СЕРВЕРА

        data_to_add = f"Response code: {response.status_code}\n"  # status code ot servera
        data_to_add = f"Response text: {response.text}\n"  # ответ от сервера
        data_to_add = f"Response headers: {headers_as_dict}\n"  # headers ot servera
        data_to_add = f"Response cookies: {cookies_as_dict}\n"  # cookies ot servera
        data_to_add = f"\n----\n"

        cls._write_log_to_file(data_to_add)  # В файл записываются данные

        # """добавим эти двам метода в my_requests в методе send"""




