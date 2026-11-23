import requests
from urls import GET_INGREDIENTS, CREATE_ORDER

class OrderMethods:
    @staticmethod
    def get_ingredients():
        return requests.get(GET_INGREDIENTS)

    @staticmethod
    def create_order(ingredient_ids: list, tokens=None):
        headers = {}
        if tokens:
            headers = tokens.auth_header
        
        payload = {'ingredients': ingredient_ids}
        return requests.post(CREATE_ORDER, json=payload, headers=headers)
