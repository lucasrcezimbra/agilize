from uuid import uuid4

import pytest

from agilize import Competence, Invoice, Invoices


@pytest.fixture
def invoices(client_mock):
    return Invoices(company_id=str(uuid4()), client=client_mock)


def test_init():
    client, company_id = object, str(uuid4())

    invoices = Invoices(company_id=company_id, client=client)

    assert invoices.client == client
    assert invoices.company_id == company_id
    assert invoices._invoices == {}


def test_iter(invoices):
    invoice1, invoice2 = object, object

    invoices._invoices = {'a': invoice1, 'b': invoice2}

    assert list(invoices) == [invoice1, invoice2]


class TestFetch:
    def test_call_client(self, invoices):
        year = 2022

        invoices.fetch(year)

        invoices.client.invoices.assert_called_once_with(
            invoices.company_id,
            year,
        )

    def test_create_invoices(self, invoices, invoices_data):
        invoices.client.invoices.return_value = invoices_data

        invoices.fetch(2022)

        assert list(invoices) == [
            Invoice.from_data(d, invoices.company_id, invoices.client)
            for d in invoices_data
        ]

    def test_ignore_invoices_without_nfse(self, invoices, invoices_data):
        data = [{**invoices_data[0], 'nfses': []}]
        invoices.client.invoices.return_value = data

        invoices.fetch(2022)

        assert list(invoices) == []


class TestGet:
    def test_get(self, invoices, invoices_data):
        data = invoices_data[0]
        another_data = {**data, 'competence': '2022-06-01T00:00:00-0300'}

        invoices.client.invoices.return_value = [data, another_data]
        competence = Competence.from_data(data['competence'])

        assert invoices.get(competence) == Invoice.from_data(
            data, invoices.company_id, invoices.client
        )

    def test_call_client(self, invoices, invoices_data):
        invoices.client.invoices.return_value = invoices_data
        competence = Competence.from_data(invoices_data[0]['competence'])

        invoices.get(competence)

        invoices.client.invoices.assert_called_once_with(
            invoices.company_id,
            competence.year,
        )

    def test_cache(self, invoices, invoices_data):
        invoices.client.invoices.return_value = invoices_data
        competence = Competence.from_data(invoices_data[0]['competence'])

        invoices.get(competence)
        invoices.get(competence)

        invoices.client.invoices.assert_called_once()
