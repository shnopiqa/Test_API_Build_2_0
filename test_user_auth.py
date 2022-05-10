import requests
import pytest  # БИБЛИОТЕКА ИСПОЛЬЗУЕТСЯ ДЛЯ ПАРАМЕТРИЗАЦИИ ТЕСТА


class TestUserAuth:
    # ПАРАМЕТРЫ ДЛЯ НЕГАТИВНОГО ТЕСТА НА АВТОРИЗАЦИЮ
    exclude_params = [
        ("no cookies"),  # ПАРАМЕТР ЗАПУСКАЕТ ТЕСТ, ГДЕ ПРОВЕРЯЕТСЯ АВТОРИЗАЦИЯ БЕЗ auth_sid
        ("no_token")  # ПАРАМЕТР ЗАПУСКАЕТ ТЕСТ, ГДЕ ПРОВЕРЯЕТСЯ АВТОРИЗАЦИЯ БЕЗ x-csrf-token
        # """ПОЗИТИВНЫЙ ТЕСТ. ПРОВЕРЯТ, ЧТО ПОЛЬЗОВАТЕЛЬ ВОШЕЛ В СИСТЕМУ"""
        #
        # """ПЕРВЫЙ ТИП ЗАПРОСА - НАПРАВЛЕННЫЙ НА ВХОД В АККАУНТ И ПОЛУЧЕНИЕ ИЗ КУКИ == auth_sid ИЗ HEADERS == x-csrf-token ИЗ JSON == USER ID"""

    ]

    def test_auth_user(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }  # Логин и пароль от аккаунта

        response1 = requests.post(
            "https://playground.learnqa.ru/api/user/login",
            data=data
        )  # request на вход в аккаунт, ИЗ НЕГО МОЖНО ПОЛУУЧИТЬ AUTH_SID, X-CSRF-TOKEN И USER_ID

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response1"  # Проверка на наличие auth_sid в куке в запрос на вход в аккаунта

        assert "x-csrf-token" in response1.headers, "There is no x-csrf-token in the response1"  # Проверка на наличие x-csrf-token в header в запросе на вход в аккаунта

        assert "user_id" in response1.json(), "There is no user_id name in the response 1"  # Проверка на наличие user_id в запросе на входе в аккаунт id юзера

        # Если проверки проходят то:
        # Для дальнейшей работы с параметрами auth_sid, x-csrf-token и user_id надо положить их в переменные

        auth_sid = response1.cookies.get("auth_sid")  # Добавляем параметр auth_sid в переменную

        token_x_csrf = response1.headers.get("x-csrf-token")  # Добавляем токен в переменную

        user_id_from_auth_method = response1.json()[
            "user_id"]  # Добавляем в переменную user_id который присваивается пользователю

        # """СОЗДАЕМ ВТОРОЙ ЗАПРОС НА ПОЛУЧЕНИЕ ДАННЫХ """

        response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                 # ЗАПРОС ГОВОРИТ О ТОМ АВТОРИЗИРОВАЛИСЬ МЫ,
                                 # ИЛИ НЕ АВТОРИЗИРОВАЛИСЬ
                                 headers={"x-csrf-token": token_x_csrf},  # ПЕРЕДАЕМ ТОКЕН В ЗАПРОС HEADERS
                                 cookies={"auth_sid": auth_sid}  # ПЕРЕДАЕМ AUTH_SID В ЗАПРОС COOKIES
                                 )
        # """ДАЛЕЕ МЫ ПРОВЕРЯЕМ ЕСТЬ ЛИ ЗНАЧЕНИЕ 'user_id' во втором запросе, и если его нету, мы возвращаем ошибку"""

        assert "user_id" in response1.json(), "THere is no user_id in response2"
        user_id_after_check = response2.json()["user_id"]  # ЗАНОСИМ user_id из response2 в отдельную переменную

        # """Проверим, что user_id из response1 равен user_id из response2"""
        # Сравниваем user_id из 1 запроса и user_id из response2, если они не равны, то ошибка

        assert user_id_from_auth_method == user_id_after_check, "user_id из response1 не равен user_id из response2"

    #
    #     """
    #     НЕГАТИВНЫЙ ТЕСТ НА ПРОВЕРКУ ДВУХ ВАРИАНТОВ:
    #     ВАРИАНТ 1: ЕСТЬ КУКИ
    #     ВАРИАНТ 2: НЕТ КУКИ
    #     ПРОВЕРКА НАПРАВЛЕННА НА ТО, ЧТОБЫ УБЕДИТСЯ ЧТО ЕСЛИ ОТПРАВИТЬ x-csrf-token, НО НЕ ОТПРАВИТЬ auth_sid -ТО ПОЛЬЗОВАТЕЛЬ НЕ АВТОРИЗУЕТСЯ 'user_id ==0'
    #     И ЕСЛИ ОТПРАВИТЬ auth_sid, но не отправлять x-csrf-token, то также мы не авторизируемся в системе, 'user_id ==0'
    #
    #     """
    #
    # """
    # ДЛЯ ТОГО, ЧТОБЫ НЕ СОЗДАВАТЬ ОДНОТИПНЫЕ ТЕСТЫ
    # ДЕЛАЕМ ПАРАМЕТРИЗАЦИЮ ТЕСТА
    # ПАРАМЕТРЫ ДЛЯ ЗАПУСКОВ ТЕСТА ВЫНОСИМ В ВВЕРХ КЛАССА
    # ПРИНЯТО ВЫНОСИТЬ ПАРАМЕТРИЗИРОВАННЫЕ ПАРАМЕТРЫ ВВЕРХУ КЛАССА
    # ПАРАМЕТРЫ НАЗОВМ EXCLUDE_PARAMS
    # ТАК ЖЕ НЕОБХОДИМО ИМПОРТИРОВАТЬ БИБЛИОТЕКУ pytest
    #      """
    #
    # """
    # В ДЕКОРАТОРЕ УКАЗЫВАЕМ СЛОВО, КОТОРОЕ БУДЕТ ВЫЗЫВАТЬ ПАРАМЕТРИЗИРОВАННЫЕ ЗАПРОСЫ И
    # ПЕРЕМЕННУЮ exclude_params В КОТОРОЙ ЛЕЖАТ ПАРАМЕТРЫ
    # """
    # """
    # В САМОЙ ФУНКЦИИ ТАК ЖЕ ПЕРЕДАЕТСЯ ПЕРЕМЕННАЯ condition, В НЕЕ ПООЧЕРЕДНО БУДУТ ПЕРЕДАВАТЬСЯ
    # ("no cookies"), #ПАРАМЕТР ЗАПУСКАЕТ ТЕСТ, ГДЕ ПРОВЕРЯЕТСЯ АВТОРИЗАЦИЯ БЕЗЫ auth_sid
    # ("no_token") #ПАРАМЕТР ЗАПУСКАЕТ ТЕСТ, ГДЕ ПРОВЕРЯЕТСЯ АВТОРИЗАЦИЯ БЕЗ x-csrf-token
    # """
    @pytest.mark.parametrize("condition", exclude_params)  # ДЕКОРАТОР pytest который позволяет параметризовать методы
    def test_negative_auth_check(self, condition):  # В ФУНКЦИИ ОБЯЗАТЕЛЬНО УКАЗЫВАТЬ СЛОВО "тест"

        # ПЕРВАЯ ЧАСТЬ НЕГАТИВНОГО ТЕСТА АНАЛОГИЧНА 1 ТЕСТУ
        # ОДНАКО USER_ID из первого запроса нам не нужен, мы будем сравнивать,
        # user_id второго запроса с 0

        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }  # Логин и пароль от аккаунта

        response1 = requests.post(
            "https://playground.learnqa.ru/api/user/login",
            data=data
        )  # request на вход в аккаунт, ИЗ НЕГО МОЖНО ПОЛУУЧИТЬ AUTH_SID, X-CSRF-TOKEN И USER_ID

        assert "auth_sid" in response1.cookies, "There is no auth cookie in the response1"  # Проверка на наличие auth_sid в куке в запрос на вход в аккаунта

        assert "x-csrf-token" in response1.headers, "There is no x-csrf-token in the response1"  # Проверка на наличие x-csrf-token в header в запросе на вход в аккаунта

        assert "user_id" in response1.json(), "There is no user_id name in the response 1"  # Проверка на наличие user_id в запросе на входе в аккаунт id юзера

        # Если проверки проходят то:
        # Для дальнейшей работы с параметрами auth_sid, x-csrf-token и user_id надо положить их в переменные

        auth_sid = response1.cookies.get("auth_sid")  # Добавляем параметр в переменную

        token_x_csrf = response1.headers.get("x-csrf-token")  # Добавляем токен в переменную

        # ДАЛЕЕ ПРОПИСЫВАЕМ УСЛОВИЯ ДЛЯ ВЫЗОВА ПАРАМЕТРОВ И СООТВЕТСТВУЮЩИХ ТЕСТОВ
        #
        # НЕГАТИВНЫЙ ТЕСТ 1: НЕТ КУКОВ, ЕСТЬ x-csrf-token

        if condition == "no_cookies":
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     # ЗАПРОС ГОВОРИТ О ТОМ АВТОРИЗИРОВАЛИСЬ МЫ,
                                     # ИЛИ НЕ АВТОРИЗИРОВАЛИСЬ
                                     headers={"x-csrf-token": token_x_csrf},  # ПЕРЕДАЕМ ТОКЕН В ЗАПРОС HEADERS
                                     )  # В ЗАПРОСЕ ПЕРЕДАЕМ ТОЛЬКО ТОКЕН

        # НЕГАТИВНЫЙ ТЕСТ 2: НЕТ x-csrf-token, ЕСТЬ auth_sid
        else:
            response2 = requests.get("https://playground.learnqa.ru/api/user/auth",
                                     # ЗАПРОС ГОВОРИТ О ТОМ АВТОРИЗИРОВАЛИСЬ МЫ,
                                     # ИЛИ НЕ АВТОРИЗИРОВАЛИСЬ
                                     cookies={"auth_sid": auth_sid}
                                     )  # ПЕРЕДАЕМ AUTH_SID В ЗАПРОС COOKIES

        # ПРОВЕРЯЕМ ЕСТЬ ЛИ USER_ID в первом методе
        # ПОЗВОЛЯЕТ ПРОВЕРИТЬ ВВЕЛИ ЛИ МЫ ПРАВИЛЬНЫЕ ДАННЫЕ ДЛЯ АВТОРИЗАЦИИ, ЕСЛИ USER_ID НЕТ ТО ТЕСТ УПАДЕТ С ОШИБКОЙ
        assert "user_id" in response1.json(), "There is no user_id in response1"

        # НАХОДИМ ЗНАЧЕНИЕ USER_ID ПОСЛЕ ПРОВЕРКИ АВТОРИЗАЦИИ БЕЗ ОДНОГО ИЗ ОБЯЗАТЕЛЬНЫХ ПАРАМЕТРОВ x-csrf-token или auth_sid
        user_id_after_check = response2.json()["user_id"]

        # ЕСЛИ МЫ ПРОХОДИМ АВТОРИЗАЦИЮ, ТО НАМ ВОЗВРАЩАЕТСЯ ОШИБКА, ЕСЛИ НЕ ПРОХОДИМ ТО ТЕСТ ПРОХОДИТ
        assert user_id_after_check == 0, f"Мы прошли авторизацию, несмотря на то что был введен только {condition}"


