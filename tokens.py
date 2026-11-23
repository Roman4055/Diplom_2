class Tokens:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @property
    def auth_header(self):
        # accessToken уже содержит "Bearer ...", ничего добавлять не нужно
        return {'Authorization': self.access_token}

    @classmethod
    def from_response(cls, response_json: dict):
        return cls(
            access_token=response_json.get('accessToken', ''),
            refresh_token=response_json.get('refreshToken', '')
        )

