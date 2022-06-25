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
    assert Client.url('info') == Client.URL_API + Client.path('info')


def test_path_prolabores():
    company_id, year = uuid4(), 2022

    path = Client.path('prolabores', company_id=company_id, year=year)
    url = Client.url('prolabores', company_id=company_id, year=year)

    assert path == Client.PATH_PROLABORE.format(company_id=company_id, year=year)
    assert url == (Client.URL_API + path)


@responses.activate
def test_info(client, info_data):
    responses.add(
        responses.GET,
        client.url('info'),
        json=info_data,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.info == info_data


@responses.activate
def test_cache_info(client, info_data):
    responses.add(responses.GET, client.url('info'), json=info_data)

    client.info
    client.info

    responses.assert_call_count(client.url('info'), 1)


@responses.activate
def test_prolabores(client, prolabores_data):
    company_id, year = uuid4(), 2022

    responses.add(
        responses.GET,
        client.url('prolabores', company_id=company_id, year=year),
        json=prolabores_data,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.prolabores(company_id, year) == prolabores_data


@responses.activate
def test_download_paycheck(client, prolabores_data):
    company_id, partner_id, year, month = uuid4(), uuid4(), 2022, 3
    file = b''

    url = Client.url(
        'download_paycheck',
        company_id=company_id,
        partner_id=partner_id,
        year=year,
        month=month,
    )

    responses.add(
        responses.GET,
        url,
        body=file,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.download_paycheck(company_id, partner_id, year, month) == file


@responses.activate
def test_partners(client, partners_data):
    company_id = uuid4()

    responses.add(
        responses.GET,
        client.url('partners', company_id=company_id),
        json=partners_data,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ],
    )

    assert client.partners(company_id) == partners_data
