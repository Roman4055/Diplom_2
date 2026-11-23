import random
import string
import pytest
import allure

from methods.user_methods import UserMethods
from tokens import Tokens

@allure.step('Сгенерировать уникальные данные пользователя')
def generate_user_data():
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return {
        'email': f'test_{suffix}@yandex.ru',
        'password': 'P@ssw0rd123',
        'name': f'Test User {suffix}'
    }

@pytest.fixture
def user_methods():
    return UserMethods()

@pytest.fixture
def registered_user(user_methods):
    """
    Создает пользователя, логинится и возвращает объект с токенами.
    Гарантированно удаляет пользователя после теста (даже если тест упал).
    """
    data = generate_user_data()
    
    # 1. Регистрация
    resp_reg = user_methods.create_user(data['email'], data['password'], data['name'])
    assert resp_reg.status_code == 200, f"Регистрация не удалась: {resp_reg.text}"
    
    # 2. Логин (чтобы получить токены и потом удалить юзера)
    resp_login = user_methods.login_user(data['email'], data['password'])
    assert resp_login.status_code == 200, f"Логин не удался: {resp_login.text}"
    
    tokens = Tokens.from_response(resp_login.json())
    
    # Формируем объект, который отдадим в тест
    user_obj = {
        'email': data['email'],
        'password': data['password'],
        'name': data['name'],
        'tokens': tokens,
        'refresh_token': tokens.refresh_token
    }
    
    yield user_obj
    
    # 3. Очистка (выполняется всегда)
    try:
        user_methods.delete_user(user_obj['tokens'].access_token)
    except Exception as e:
        print(f"Не удалось удалить пользователя после теста: {e}")
