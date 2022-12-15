from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from agilize import Competence, Tax
from agilize.agilize import DATETIME_FORMAT


@pytest.fixture
def tax(faker, client_mock):
    return Tax(
        abbreviation=faker.name(),
        amount=faker.pydecimal(),
        client=client_mock,
        company_id=str(uuid4()),
        competence=Competence(faker.year(), faker.month()),
        due_date=faker.date_object(),
        id=str(uuid4()),
    )


def test_from_data(taxes_data):
    company_id, client, data = str(uuid4()), object, taxes_data[0]

    tax = Tax.from_data(data, company_id, client)

    assert tax.abbreviation == data['taxAbbreviation']
    assert tax.amount == Decimal(str(data['total']))
    assert tax.client == client
    assert tax.company_id == company_id
    assert tax.competence == Competence.from_data(data['competence'])
    assert tax.due_date == datetime.strptime(data['deadline'], DATETIME_FORMAT).date()
    assert tax.id == data['__identity']


def test_download(tax):
    tax.download()

    tax.client.download_tax.assert_called_once_with(tax.company_id, tax.id)
