from uuid import uuid4

import pytest
import requests
import responses

from agilize.keycloak import Keycloak


@pytest.fixture
def keycloak():
    base_url = 'https://sso.agilize.com.br/auth/'
    client_id = 'agilize-legacy-client'
    realm_name = 'AgilizeAPPs'
    return Keycloak(base_url, client_id, realm_name)


def test_init():
    keycloak = Keycloak('BASE_URL', 'CLIENT_ID', 'REALM_NAME')

    assert keycloak.base_url == 'BASE_URL'
    assert keycloak.client_id == 'CLIENT_ID'
    assert keycloak.realm_name == 'REALM_NAME'
    assert isinstance(keycloak.session, requests.Session)


def test_path(keycloak):
    assert keycloak.path('token') == Keycloak.PATH_TOKEN.format(realm_name=keycloak.realm_name)


def test_url(keycloak):
    assert keycloak.url('token') == keycloak.base_url + keycloak.path('token')


def test_url_base_without_slash(keycloak):
    keycloak.base_url = 'https://sso.agilize.com.br/auth'
    assert keycloak.url('token') == 'https://sso.agilize.com.br/auth/' + keycloak.path('token')


def test_token_call_post(keycloak, mocker):
    post_spy = mocker.patch('requests.Session.post')

    username, password = 'cnpj', 'password'
    keycloak.token(username, password)

    post_spy.assert_called_once_with(
        keycloak.url('token'),
        data={
            "username": username,
            "password": password,
            "client_id": keycloak.client_id,
            "grant_type": ['password'],
        }
    )


@responses.activate
def test_token(keycloak):
    response = {
        'access_token': 'random_string',
        'expires_in': 600,
        'refresh_expires_in': 1800,
        'refresh_token': 'other_random_string',
        'token_type': 'Bearer',
        'not-before-policy': 0,
        'session_state': str(uuid4()),
        'scope': 'profile roles email'
    }
    responses.add(responses.POST, keycloak.url('token'), json=response)

    assert keycloak.token('username', 'password') == response
