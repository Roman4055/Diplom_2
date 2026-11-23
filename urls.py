BASE_URL = 'https://stellarburgers.education-services.ru/api'

# Auth & User
CREATE_USER = f'{BASE_URL}/auth/register'
LOGIN_USER = f'{BASE_URL}/auth/login'
LOGOUT_USER = f'{BASE_URL}/auth/logout'
REFRESH_TOKEN = f'{BASE_URL}/auth/token'
DELETE_USER = f'{BASE_URL}/auth/user'  # Если есть в документации для очистки

# Order
GET_INGREDIENTS = f'{BASE_URL}/ingredients'
CREATE_ORDER = f'{BASE_URL}/orders'
