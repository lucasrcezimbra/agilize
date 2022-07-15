from uuid import uuid4

import pytest

from agilize import Competence, Tax, Taxes


@pytest.fixture
def taxes(client_mock):
    return Taxes(company_id=str(uuid4()), client=client_mock)


def test_init():
    client, company_id = object, str(uuid4())

    taxes = Taxes(company_id=company_id, client=client)

    assert taxes.client == client
    assert taxes.company_id == company_id
    assert taxes._taxes_by_competence == {}


def test_iter(taxes):
    tax1, tax2, tax3 = object, object, object

    taxes._taxes_by_competence = {'1': {'a': tax1, 'b': tax2}, '2': {'c': tax3}}

    assert list(taxes) == [tax1, tax2, tax3]


class TestFetch:
    def test_call_client(self, taxes):
        year = 2022

        taxes.fetch(year)

        taxes.client.taxes.assert_called_once_with(
            taxes.company_id,
            year,
        )

    def test_create_taxes(self, taxes, taxes_data):
        taxes.client.taxes.return_value = taxes_data

        taxes.fetch(2022)

        assert list(taxes) == [
            Tax.from_data(d, taxes.company_id, taxes.client)
            for d in taxes_data
        ]


class TestGet:
    def test_call_client(self, taxes, taxes_data):
        taxes.client.taxes.return_value = taxes_data
        abbreviation = taxes_data[0]['taxAbbreviation']
        competence = Competence.from_data(taxes_data[0]['competence'])

        taxes.get(abbreviation, competence)

        taxes.client.taxes.assert_called_once_with(
            taxes.company_id,
            competence.year,
        )

    def test_cache(self, taxes, taxes_data):
        taxes.client.taxes.return_value = taxes_data
        abbreviation = taxes_data[0]['taxAbbreviation']
        competence = Competence.from_data(taxes_data[0]['competence'])

        taxes.get(abbreviation, competence)
        taxes.get(abbreviation, competence)

        taxes.client.taxes.assert_called_once()
