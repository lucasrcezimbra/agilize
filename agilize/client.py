import requests

from agilize.keycloak import Keycloak


class URL:
    BASE = 'https://app.agilize.com.br/api/v1/'

    DOWNLOAD_PROLABORE = BASE + 'companies/{company_id}/prolabore-anual/download'
    DOWNLOAD_TAX = BASE + 'companies/{company_id}/taxes/{tax_id}/billet'
    INFO = BASE + 'companies/security-user/info'
    INVOICES = BASE + 'companies/{company_id}/invoices'
    INVOICE_PAYMENT = BASE + 'companies/{company_id}/invoices/{invoice_id}'
    PARTNERS = BASE + 'companies/{company_id}/partners'
    PROLABORE = BASE + 'companies/{company_id}/prolabore-anual'
    TAXES = BASE + 'companies/{company_id}/taxes'
    UPLOAD_NFSE = BASE + 'companies/{company_id}/nfseimportresources'
    UPLOAD_NFSE2 = BASE + 'companies/{company_id}/nfses/importfromresource'


class AnonymousClient:
    @staticmethod
    def download(url):
        return requests.get(url).content


class Client(AnonymousClient):
    AUTH_URL = 'https://sso.agilize.com.br/auth/'
    CLIENT_ID = 'agilize-legacy-client'
    REALM_NAME = 'AgilizeAPPs'

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
                url=URL.INFO,
                headers=self.headers,
            )
            self._info = response.json()
        return self._info

    @property
    def headers(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    def partners(self, company_id):
        response = requests.get(
            url=URL.PARTNERS.format(company_id=company_id),
            headers=self.headers,
        )
        return response.json()

    def prolabores(self, company_id, year):
        response = requests.get(
            url=URL.PROLABORE.format(company_id=company_id),
            params={'anoReferencia': f'{year}-01-01T00:00:00P'},
            headers=self.headers,
        )
        return response.json()

    def download_prolabore(self, company_id, partner_id, year, month):
        response = requests.get(
            url=URL.DOWNLOAD_PROLABORE.format(company_id=company_id),
            params={
                'competence': f'{year}-{month}-01T00:00:00-0300',
                'partner': partner_id,
            },
            headers=self.headers,
        )
        return response.content

    def taxes(self, company_id, year):
        response = requests.get(
            url=URL.TAXES.format(company_id=company_id),
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
            url=URL.DOWNLOAD_TAX.format(company_id=company_id, tax_id=tax_id),
            headers=self.headers,
        )
        return self.download(response.json()['url'])

    def invoices(self, company_id, year):
        response = requests.get(
            url=URL.INVOICES.format(company_id=company_id),
            params={
                'count': 3000,
                'page': 1,
                'year': year,
            },
            headers=self.headers,
        )
        return response.json()

    def invoice_payment(self, company_id, invoice_id):
        response = requests.get(
            url=URL.INVOICE_PAYMENT.format(company_id=company_id, invoice_id=invoice_id),
            headers=self.headers,
        )
        return response.json()

    def upload_nfse(self, company_id, filebytes):
        response = requests.post(
            url=URL.UPLOAD_NFSE.format(company_id=company_id),
            files={'resources[0]': ('whatever.xml', filebytes, 'text/xml')},
            headers=self.headers,
        )
        response2 = requests.post(
            url=URL.UPLOAD_NFSE2.format(company_id=company_id),
            json={'nfseImportResource': response.json()['__identity']},
            headers=self.headers,
        )
        return response2.json()
