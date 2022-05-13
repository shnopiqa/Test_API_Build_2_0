import requests
from lib.my_requests import MyRequests
from lib.assertions import Assertions
from lib.base_case import BaseCase


# """Метод будет проверять API на получение информации о пользователе"""

class TestUserGet(BaseCase):
    # """МЕТОД ПРОВЕРЯЕТ ЧТО МОЖНО ПОЛУЧИТЬ ДАННЫЕ О ПОЛЬЗОВТАЕЛЬ БЕЗ АВТОРИЗАЦИИ"""
    def test_get_user_info_not_auth(self):
        response1 = MyRequests.get("/user/2")  # При запросе без авторизации метод возвращает только Username
        # """создаим новый метод в классе Assertions который будет проверять что каких=то полей нет по названию"""
        # Assertions.assert_json_has_no_key(response1,"username")
        # Assertions.assert_json_has_no_key(response1, "email")
        # Assertions.assert_json_has_no_key(response1, "firstName")
        # Assertions.assert_json_has_no_key(response1, "LastName")
        # ВЫЗЫВАЯ ДАННУЮ ПРОВЕРКУ МЫ УБЕЖДАЕМСЯ, ЧТО В ОТВЕТЕ НЕТУ ВВЕДЕННЫХ ЗНАЧЕНИЙ, ЕСЛИ ОНИ ЕСТЬ, ПОЯВЛЯЕТСЯ ОШИБКА
        # замени проверку через 1 ключ, проверкой через список
        keys_that_not_view_in_response_1 = ["email", "firstName", "lastName"]
        Assertions.assert_json_has_no_any_keys(response1,
        keys_that_not_view_in_response_1) #проверяет, что нет ключа, которого не должно быть в JSON

        # print(response1.content)

    # """НАПИШЕМ МЕТОД КОТОРЫЙ ПРОВЕРЯЕТ ДАННЫЕ КОТОРЫЕ ДАЕТ СЕРВИС ПРИ АВТОРИЗИРОВАННОМ ПОЛЬЗОВАТЕЛЕ"""

    def test_get_user_info_auth(self):
        email = "vinkotov@example.com"
        data = {

            "password": "1234",
            "username": "learnqa",
            "firstName": "learnqa",
            "lastName": "learnqa",
            "email": email  # ВВЕДЕН ЭМЭЙЛ, КОТОРЫЙ УЖЕ ЗАРЕГИСТРИРОВАН В СИСТЕМЕ
        }
        response2 = MyRequests.post("/user/login",
                                    data=data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token_x_csrf = self.get_header(response2, "x-csrf-token")
        user_id_from_auth_method = self.get_json_value(response2, "user_id")
        response3 = MyRequests.get(f"/user/{user_id_from_auth_method}",
                                   headers={"x-csrf-token": token_x_csrf},
                                   cookies={"auth_sid": auth_sid}
                                   )
        # """В ASSERTION можно написать assert_json_has_keys - метод который бдует проверять сразу весь набор данных который
        # должен содержать ответ JSON"""
        # заменим проверку наличия полей, 1 методом, который проверяет список из полей в JSON
        # Assertions.assert_json_has_key(response3,"username")
        # Assertions.assert_json_has_key(response3, "email")
        # Assertions.assert_json_has_key(response3, "firstName")
        # Assertions.assert_json_has_key(response3, "LastName")

        #МЕТОД ПРОВЕРЯЕТ СПИСОК НА НАЛИЧИЕ ПОЛЕЙ В JSON
        expected_value_fields_response_3 = ["username", "email", "firstName", "lastName"]
        Assertions.assert_json_has_more_then_one_keys(response3,expected_value_fields_response_3)

        #ОШИБКИ КОТОРЫЙ БЫЛИ ИСПРАВЛЕНЫ: LastName заменил на lastName, неправильно назвал токен, направильно указал метод


