import requests
from urls import CREATE_USER, LOGIN_USER, LOGOUT_USER, REFRESH_TOKEN, DELETE_USER
from tokens import Tokens


class UserMethods:
    @staticmethod
    def create_user(email: str, password: str, name: str):
        # Поля со значением None не включаем в payload:
        # отправка 'email': null — это не «отсутствующее поле»,
        # а другой сценарий, который сервер может обрабатывать иначе.
        payload = {
            key: value
            for key, value in {'email': email, 'password': password, 'name': name}.items()
            if value is not None
        }
        return requests.post(CREATE_USER, json=payload)

    @staticmethod
    def login_user(email: str, password: str):
        payload = {'email': email, 'password': password}
        return requests.post(LOGIN_USER, json=payload)

    @staticmethod
    def logout_user(refresh_token: str):
        payload = {'token': refresh_token}
        return requests.post(LOGOUT_USER, json=payload)

    @staticmethod
    def refresh_access_token(refresh_token: str):
        payload = {'token': refresh_token}
        return requests.post(REFRESH_TOKEN, json=payload)

    @staticmethod
    def delete_user(access_token: str):
        headers = {'Authorization': access_token}  # без добавления Bearer
        return requests.delete(DELETE_USER, headers=headers)
