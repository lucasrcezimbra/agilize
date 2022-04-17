from uuid import uuid4

import pytest
import responses
from responses import matchers

from agilize.client import Client
from agilize.keycloak import Keycloak


@pytest.fixture
def info_data():
    return {
        'accountIdentifier': '12345678000160',
        'creationDate': '2022-04-17T17:11:00-0300',
        'expirationDate': None,
        'party': {
            'companies': [
                {
                    'activityType': 1,
                    'city': {'code': '1234567', 'name': 'Porto Alegre'},
                    'clientSince': '2022-04-17T17:11:00-0300',
                    'cnpj': '12345678000160',
                    'email': 'example@email.com',
                    'firstEmail': 'example@email.com',
                    'foundingDate': '2022-04-17T17:13:00-0300',
                    'hasEmployees': False,
                    'hasFinanceiro': True,
                    'isAgilizePremium': False,
                    'isBlocked': False,
                    'isComercio': False,
                    'isHabilitadoEmitirNfse': False,
                    'isLucroPresumido': False,
                    'isMei': False,
                    'isOperadoPorProcuracao': False,
                    'lockedAt': None,
                    'name': 'PYTHON LTDA',
                    '__identity': str(uuid4()),
                }
            ],
            'email': 'example@email.com',
            'emailIsVerified': True,
            'name': None,
            'temporaryEmail': None,
            '__identity': str(uuid4()),
        },
        'roles': {
            'Agilize.Api:Customer': {
                'identifier': 'Agilize.Api:Customer',
                'name': 'Customer',
            }
        },
    }


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


def test_url(client):
    assert client.url('info') == Client.URL_API + client.path('info')


@responses.activate
def test_info(client, info_data):
    responses.add(
        responses.GET,
        client.url('info'),
        json=info_data,
        match=[
            matchers.header_matcher({"Authorization": f"Bearer {client.access_token}"})
        ]
    )

    assert client.info == info_data


@responses.activate
def test_cache_info(client, info_data):
    responses.add(responses.GET, client.url('info'), json=info_data)

    client.info
    client.info

    responses.assert_call_count(client.url('info'), 1)
