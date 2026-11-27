import pytest
import allure
from methods.order_methods import OrderMethods

class TestCreateOrder:
    
    @pytest.fixture
    def order_methods(self):
        return OrderMethods()

    @pytest.fixture
    def valid_ingredient_ids(self, order_methods):
        resp = order_methods.get_ingredients()
        assert resp.status_code == 200
        data = resp.json()
        # Берем первые 3 ингредиента для теста
        return [item['_id'] for item in data['data'][:3]]

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_authorized(self, registered_user, order_methods, valid_ingredient_ids):
        resp = order_methods.create_order(valid_ingredient_ids, tokens=registered_user['tokens'])
        assert resp.status_code == 200
        data = resp.json()
        assert data['success'] is True
        assert 'order' in data
        assert 'number' in data['order']

    @allure.title("Создание заказа без авторизации (заказ проходит, но анонимный)")
    def test_create_order_unauthorized(self, order_methods, valid_ingredient_ids):
        resp = order_methods.create_order(valid_ingredient_ids, tokens=None)
        # Фактическое поведение API: заказы без токена разрешены (редирект
        # на /login происходит только в интерфейсе, а не в API)
        assert resp.status_code == 200
        data = resp.json()
        assert data['success'] is True
        assert 'number' in data['order']

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_empty_ingredients(self, registered_user, order_methods):
        resp = order_methods.create_order([], tokens=registered_user['tokens'])
        # Обычно пустой список ингредиентов сервер отвергает с 400
        assert resp.status_code == 400

    @allure.title("Создание заказа с неверным хешем ингредиента (500 Internal Server Error)")
    def test_create_order_invalid_hash(self, registered_user, order_methods):
        # Передаем несуществующий хеш вместо валидного ID
        resp = order_methods.create_order(['invalid_hash_123'], tokens=registered_user['tokens'])

        # Фактическое поведение API: сервер не обрабатывает невалидный хеш
        # и падает с 500. Тело ответа — HTML-страница ошибки, а не JSON,
        # поэтому resp.json() здесь не вызываем.
        assert resp.status_code == 500
