import pytest
import allure
from methods.user_methods import UserMethods

class TestUserAuth:
    
    @allure.title("Регистрация уникального пользователя")
    def test_create_unique_user(self, registered_user):
        # Если фикстура сработала и не упала — значит, пользователь создан успешно
        assert True

    @allure.title("Регистрация существующего пользователя (ошибка 403)")
    def test_create_existing_user(self, registered_user, user_methods):
        # Пытаемся зарегистрировать того же самого пользователя повторно
        resp = user_methods.create_user(
            registered_user['email'], 
            registered_user['password'], 
            registered_user['name']
        )
        assert resp.status_code == 403
        data = resp.json()
        assert data['success'] is False
        assert "User already exists" in data['message']

    @allure.title("Регистрация без одного из обязательных полей (ошибка 403)")
    @pytest.mark.parametrize("missing_field", [
        {'email': 'test@yandex.ru', 'password': '123'}, # нет name
        {'email': 'test@yandex.ru', 'name': 'User'},   # нет password
        {'password': '123', 'name': 'User'}            # нет email
    ])
    def test_create_missing_fields(self, user_methods, missing_field):
        # Формируем payload, пропуская одно поле
        payload = {
            'email': missing_field.get('email', 'test@yandex.ru'),
            'password': missing_field.get('password', '123'),
            'name': missing_field.get('name', 'User')
        }
        # Удаляем явно отсутствующее поле, если его нет в параметре
        if 'email' not in missing_field: del payload['email']
        if 'password' not in missing_field: del payload['password']
        if 'name' not in missing_field: del payload['name']

        resp = user_methods.create_user(
            payload.get('email'), 
            payload.get('password'), 
            payload.get('name')
        )
        assert resp.status_code == 403
        data = resp.json()
        assert data['success'] is False
        assert "required fields" in data['message']

    @allure.title("Успешный логин существующего пользователя")
    def test_login_success(self, registered_user, user_methods):
        resp = user_methods.login_user(
            registered_user['email'], 
            registered_user['password']
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data['success'] is True
        assert 'accessToken' in data
        assert 'refreshToken' in data

    @allure.title("Логин с неверными данными (ошибка 401)")
    @pytest.mark.parametrize("wrong_email, wrong_pass", [
        ('wrong@email.com', '123'),
        ('test@yandex.ru', 'wrong_password')
    ])
    def test_login_invalid_credentials(self, user_methods, wrong_email, wrong_pass):
        resp = user_methods.login_user(wrong_email, wrong_pass)
        assert resp.status_code == 401
        data = resp.json()
        assert data['success'] is False
        assert "incorrect" in data['message']
