from uuid import uuid4

import pytest

from agilize import Competence, Tax


@pytest.fixture
def tax(faker, client_mock):
    return Tax(
        abbreviation=faker.name(),
        client=client_mock,
        company_id=str(uuid4()),
        competence=Competence(faker.year(), faker.month()),
        id=str(uuid4()),
    )


def test_from_data(taxes_data):
    company_id, client, data = str(uuid4()), object, taxes_data[0]

    tax = Tax.from_data(data, company_id, client)

    assert tax.abbreviation == data['taxAbbreviation']
    assert tax.client == client
    assert tax.company_id == company_id
    assert tax.competence == Competence.from_data(data['competence'])
    assert tax.id == data['__identity']


def test_download(tax):
    tax.download()

    tax.client.download_tax.assert_called_once_with(tax.company_id, tax.id)
