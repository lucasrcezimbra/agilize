from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from agilize import Competence, Invoice
from agilize.agilize import DATETIME_FORMAT


@pytest.fixture
def invoice(faker):
    return Invoice(
        amount=faker.pydecimal(),
        competence=Competence(faker.year(), faker.month()),
        client=object,
        due_date=faker.date_object(),
        id=str(uuid4()),
        url_nfse=faker.url(),
    )


def test_from_data(invoices_data):
    client, data = object, invoices_data[0]

    invoice = Invoice.from_data(data, client)

    assert invoice.amount == Decimal(str(data['total']))
    assert invoice.competence == Competence.from_data(data['competence'])
    assert invoice.client == client
    assert invoice.due_date == datetime.strptime(data['deadline'], DATETIME_FORMAT).date()
    assert invoice.id == data['__identity']
    assert invoice.url_nfse == data['nfses'][0]['nfseUrl']


def test_url_nfse_image(invoice, faker):
    invoice.url_nfse = (
        'https://nfse.salvador.ba.gov.br/site/contribuinte/nota/notaprint.aspx'
        f'?nf={faker.pyint()}'
        f'&inscricao={faker.pyint()}'
        f'&verificacao={faker.pystr()}'
    )

    assert invoice.url_nfse_image == invoice.url_nfse.replace('notaprint', 'notaprintimg')


def test_download_nfse(invoice, mocker):
    anonymous_client_mock = mocker.patch('agilize.agilize.AnonymousClient')

    invoice.download_nfse()

    anonymous_client_mock.download.assert_called_once_with(invoice.url_nfse_image)
