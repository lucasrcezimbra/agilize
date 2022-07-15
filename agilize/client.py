import requests

from agilize.keycloak import Keycloak


class Client:
    AUTH_URL = 'https://sso.agilize.com.br/auth/'
    CLIENT_ID = 'agilize-legacy-client'
    REALM_NAME = 'AgilizeAPPs'

    URL_API = 'https://app.agilize.com.br/api/v1/'
    PATH_DOWNLOAD_PROLABORE = 'companies/{company_id}/prolabore-anual/download'
    PATH_DOWNLOAD_TAX = 'companies/{company_id}/taxes/{tax_id}/billet'
    PATH_INFO = 'companies/security-user/info'
    PATH_INVOICES = 'companies/{company_id}/invoices'
    PATH_PARTNERS = 'companies/{company_id}/partners'
    PATH_PROLABORE = 'companies/{company_id}/prolabore-anual'
    PATH_TAXES = 'companies/{company_id}/taxes'

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
            response = requests.get(
                url=self.url(self.PATH_INFO),
                headers=self.headers,
            )
            self._info = response.json()
        return self._info

    @property
    def headers(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def partners(self, company_id):
        response = requests.get(
            url=self.url(self.PATH_PARTNERS, company_id=company_id),
            headers=self.headers,
        )
        return response.json()

    def prolabores(self, company_id, year):
        response = requests.get(
            url=self.url(self.PATH_PROLABORE, company_id=company_id),
            params={'anoReferencia': f'{year}-01-01T00:00:00P'},
            headers=self.headers,
        )
        return response.json()

    def download_prolabore(self, company_id, partner_id, year, month):
        response = requests.get(
            url=self.url(self.PATH_DOWNLOAD_PROLABORE, company_id=company_id),
            params={
                'competence': f'{year}-{month}-01T00:00:00-0300',
                'partner': partner_id,
            },
            headers=self.headers,
        )
        return response.content

    def taxes(self, company_id, year):
        response = requests.get(
            url=self.url(self.PATH_TAXES, company_id=company_id),
            params={
                'blocking': True,
                'closed': True,
                'count': 3000,
                'direction': 'desc',
                'onlyTaxesNotProvisionedByRh': True,
                'page': 1,
                'sort': 'companyTax.competence',
                'year': year,
            },
            headers=self.headers,
        )
        return response.json()

    def download_tax(self, company_id, tax_id):
        response = requests.get(
            url=self.url(self.PATH_DOWNLOAD_TAX, company_id=company_id, tax_id=tax_id),
            headers=self.headers,
        )
        file_url = response.json()['url']
        return requests.get(file_url).content

    def invoices(self, company_id, year):
        response = requests.get(
            url=self.url(self.PATH_INVOICES, company_id=company_id),
            params={
                'count': 3000,
                'page': 1,
                'year': year,
            },
            headers=self.headers,
        )
        return response.json()

    @classmethod
    def url(cls, path, **kwargs):
        return cls.URL_API + path.format(**kwargs)
