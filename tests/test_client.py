from uuid import uuid4

import pytest
import responses
from responses import matchers

from agilize import Client
from agilize.client import URL
from agilize.keycloak import Keycloak


@pytest.fixture
def client(mocker):
    return Client('john', 'p4ssw0rd', keycloak=mocker.create_autospec(Keycloak))


def test_init(mocker):
    keycloak_mock = mocker.patch('agilize.client.Keycloak', autospec=True)

    client = Client('john', 'p4ssw0rd')

    assert client.username == 'john'
    assert client.password == 'p4ssw0rd'
    keycloak_mock.assert_called_once_with(
        Client.AUTH_URL, Client.CLIENT_ID, Client.REALM_NAME
    )


def test_access_token(client, mocker):
    access_token = 'random_string'
    client.keycloak.token.return_value = {'access_token': access_token}

    assert client.access_token == access_token
    client.keycloak.token.assert_called_once_with(client.username, client.password)


def test_cache_access_token(client):
    client.access_token
    client.keycloak.token.assert_called_once()

    client.keycloak.token.reset_mock()
    client.access_token
    client.keycloak.token.assert_not_called()


@responses.activate
def test_info(client, info_data):
    responses.add(
        responses.GET,
        URL.INFO,
        json=info_data,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.info == info_data


@responses.activate
def test_cache_info(client, info_data):
    responses.add(responses.GET, URL.INFO, json=info_data)

    client.info
    client.info

    responses.assert_call_count(URL.INFO, 1)


@responses.activate
def test_prolabores(client, prolabores_data):
    company_id, year = uuid4(), 2022

    responses.add(
        responses.GET,
        URL.PROLABORE.format(company_id=company_id),
        json=prolabores_data,
        match=[
            matchers.query_string_matcher(f'anoReferencia={year}-01-01T00:00:00P'),
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.prolabores(company_id, year) == prolabores_data


@responses.activate
def test_download_prolabore(client, prolabores_data):
    company_id, partner_id, year, month = uuid4(), uuid4(), 2022, 3
    file = b''

    responses.add(
        responses.GET,
        URL.DOWNLOAD_PROLABORE.format(company_id=company_id),
        body=file,
        match=[
            matchers.query_string_matcher(
                f'competence={year}-{month}-01T00:00:00-0300&partner={partner_id}'
            ),
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.download_prolabore(company_id, partner_id, year, month) == file


@responses.activate
def test_partners(client, partners_data):
    company_id = uuid4()

    responses.add(
        responses.GET,
        URL.PARTNERS.format(company_id=company_id),
        json=partners_data,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.partners(company_id) == partners_data


@responses.activate
def test_taxes(client, taxes_data):
    company_id, year = uuid4(), 2022

    responses.add(
        responses.GET,
        URL.TAXES.format(company_id=company_id),
        json=taxes_data,
        match=[
            matchers.query_param_matcher(
                {
                    'blocking': True,
                    'closed': True,
                    'count': 3000,
                    'direction': 'desc',
                    'onlyTaxesNotProvisionedByRh': True,
                    'page': 1,
                    'sort': 'companyTax.competence',
                    'year': year,
                },
            ),
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.taxes(company_id, year) == taxes_data


@responses.activate
def test_invoices(client, invoices_data):
    company_id, year = uuid4(), 2022

    responses.add(
        responses.GET,
        URL.INVOICES.format(company_id=company_id),
        json=invoices_data,
        match=[
            matchers.query_param_matcher({'count': 3000, 'page': 1, 'year': year}),
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.invoices(company_id, year) == invoices_data


@responses.activate
def test_download_tax(client, faker, prolabores_data):
    company_id, tax_id = uuid4(), uuid4()
    file_url = faker.url()
    file = b''

    responses.add(
        responses.GET,
        URL.DOWNLOAD_TAX.format(company_id=company_id, tax_id=tax_id),
        json={'url': file_url},
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )
    responses.add(responses.GET, file_url, body=file)

    assert client.download_tax(company_id, tax_id) == file


@responses.activate
def test_upload_invoice(client, faker):
    company_id = uuid4()
    file = b''
    file_identity = str(uuid4())
    expected_response = {
        'countNfses': 1,
        'createdAt': '2022-10-29T14:40:00-0300',
        'nfses': [],
    }

    responses.add(
        responses.POST,
        URL.UPLOAD_NFSE.format(company_id=company_id),
        json={'__identity': file_identity},
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"}),
            matchers.multipart_matcher({'resources[0]': ('whatever.xml', file, 'text/xml')}),
        ],
    )
    responses.add(
        responses.POST,
        URL.UPLOAD_NFSE2.format(company_id=company_id),
        json=expected_response,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"}),
            matchers.json_params_matcher({"nfseImportResource": file_identity}),
        ],
    )

    assert client.upload_nfse(company_id, file) == expected_response


@responses.activate
def test_invoice_payment(client, invoice_payment_data):
    company_id, invoice_id = uuid4(), uuid4()

    responses.add(
        responses.GET,
        URL.INVOICE_PAYMENT.format(company_id=company_id, invoice_id=invoice_id),
        json=invoice_payment_data,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.invoice_payment(company_id, invoice_id) == invoice_payment_data
