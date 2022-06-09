import pytest

from agilize import Agilize
from agilize.agilize import Company


@pytest.fixture
def agilize(client_mock):
    return Agilize('username', 'p4ssw0rd', client=client_mock)


def test_init(mocker):
    client_mock = mocker.patch('agilize.agilize.Client', autospec=True)

    Agilize('username', 'p4ssw0rd')

    client_mock.assert_called_once_with('username', 'p4ssw0rd')


def test_companies(agilize, info_data):
    agilize.client.info = info_data

    companies = agilize.companies()

    company_data = info_data['party']['companies'][0]
    assert len(companies) == len(info_data['party']['companies'])
    assert len(companies) == 1
    assert companies[0] == Company(
        id=company_data['__identity'],
        cnpj=company_data['cnpj'],
        name=company_data['name'],
        client=agilize.client,
    )
