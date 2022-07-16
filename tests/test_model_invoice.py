import pytest

from agilize import Competence, Invoice


@pytest.fixture
def invoice(faker):
    return Invoice(
        competence=Competence(faker.year(), faker.month()),
        url_nfse=faker.url(),
    )


def test_from_data(invoices_data):
    data = invoices_data[0]

    invoice = Invoice.from_data(data)

    assert invoice.competence == Competence.from_data(data['competence'])
    assert invoice.url_nfse == data['nfses'][0]['nfseUrl']


def test_download_nfse(invoice, mocker):
    anonymous_client_mock = mocker.patch('agilize.agilize.AnonymousClient')

    invoice.download_nfse()

    anonymous_client_mock.download.assert_called_once_with(invoice.url_nfse)
