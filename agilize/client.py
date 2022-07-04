import requests

from agilize.keycloak import Keycloak


class Client:
    AUTH_URL = 'https://sso.agilize.com.br/auth/'
    CLIENT_ID = 'agilize-legacy-client'
    REALM_NAME = 'AgilizeAPPs'

    URL_API = 'https://app.agilize.com.br/api/v1/'
    PATH_INFO = 'companies/security-user/info'
    PATH_PARTNERS = 'companies/{company_id}/partners'
    PATH_PROLABORE = 'companies/{company_id}/prolabore-anual?anoReferencia={year}-01-01T00:00:00P'
    PATH_DOWNLOAD_PAYCHECK = (
        'companies/{company_id}/prolabore-anual/download'
        '?competence={year}-{month}-01T00:00:00-0300&partner={partner_id}'
    )

    def __init__(self, username, password, keycloak=None):
        self.username = username
        self.password = password
        self.keycloak = keycloak or Keycloak(self.AUTH_URL, self.CLIENT_ID, self.REALM_NAME)
        self._access_token = None
        self._info = None

    @property
    def access_token(self):
        if not self._access_token:
            token = self.keycloak.token(self.username, self.password)
            self._access_token = token['access_token']
        return self._access_token

    @property
    def info(self):
        if not self._info:
            response = requests.get(url=self.url(self.PATH_INFO), headers=self.headers)
            self._info = response.json()
        return self._info

    @property
    def headers(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def partners(self, company_id):
        url = self.url(self.PATH_PARTNERS, company_id=company_id)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def prolabores(self, company_id, year):
        url = self.url(self.PATH_PROLABORE, company_id=company_id, year=year)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def download_paycheck(self, company_id, partner_id, year, month):
        url = self.url(
            self.PATH_DOWNLOAD_PAYCHECK,
            company_id=company_id,
            partner_id=partner_id,
            year=year,
            month=month,
        )
        response = requests.get(url=url, headers=self.headers)
        return response.content

    @classmethod
    def url(cls, path, **kwargs):
        return cls.URL_API + path.format(**kwargs)
