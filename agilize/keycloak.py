import requests


def urljoin(p1, p2):
    if not p1.endswith('/'):
        p1 += '/'
    return p1 + p2


class Keycloak:
    # TODO: add refresh_token
    PATH_TOKEN = "realms/{realm_name}/protocol/openid-connect/token"

    def __init__(self, base_url, client_id, realm_name):
        self.base_url = base_url
        self.client_id = client_id
        self.realm_name = realm_name
        self.session = requests.Session()

    def token(self, username, password):
        url = self.base_url + self.PATH_TOKEN.format(realm_name=self.realm_name)
        payload = {
            "username": username,
            "password": password,
            "client_id": self.client_id,
            "grant_type": ['password'],
        }
        return self.session.post(url, data=payload).json()

    def url(self, type):
        return urljoin(self.base_url, self.path(type))

    def path(self, type):
        return {
            'token': self.PATH_TOKEN.format(realm_name=self.realm_name),
        }[type]
