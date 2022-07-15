from uuid import uuid4

import pytest
import responses
from responses import matchers

from agilize import Client
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


def test_url():
    assert Client.url(Client.PATH_INFO) == (Client.URL_API + Client.PATH_INFO)


def test_url_with_params():
    company_id = uuid4()

    url = Client.url(Client.PATH_PROLABORE, company_id=company_id)

    assert url == (Client.URL_API + f'companies/{company_id}/prolabore-anual')


@responses.activate
def test_info(client, info_data):
    responses.add(
        responses.GET,
        client.url(Client.PATH_INFO),
        json=info_data,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.info == info_data


@responses.activate
def test_cache_info(client, info_data):
    responses.add(responses.GET, client.url(Client.PATH_INFO), json=info_data)

    client.info
    client.info

    responses.assert_call_count(client.url(Client.PATH_INFO), 1)


@responses.activate
def test_prolabores(client, prolabores_data):
    company_id, year = uuid4(), 2022

    responses.add(
        responses.GET,
        client.url(Client.PATH_PROLABORE, company_id=company_id),
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

    url = Client.url(Client.PATH_DOWNLOAD_PROLABORE, company_id=company_id)

    responses.add(
        responses.GET,
        url,
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
        client.url(Client.PATH_PARTNERS, company_id=company_id),
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
        client.url(Client.PATH_TAXES, company_id=company_id),
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
        client.url(Client.PATH_INVOICES, company_id=company_id),
        json=invoices_data,
        match=[
            matchers.query_param_matcher({'count': 3000, 'page': 1, 'year': year}),
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.invoices(company_id, year) == invoices_data
