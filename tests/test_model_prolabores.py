from uuid import uuid4

import pytest

from agilize import Competence, Prolabore, Prolabores


@pytest.fixture
def prolabores(client_mock):
    return Prolabores(company_id=str(uuid4()), client=client_mock)


def test_init():
    client = object
    company_id = str(uuid4())

    prolabores = Prolabores(company_id=company_id, client=client)

    assert prolabores.client == client
    assert prolabores.company_id == company_id
    assert prolabores._prolabores == {}


def test_iter(prolabores):
    prolabore1 = object
    prolabore2 = object

    prolabores._prolabores = {'1': prolabore1, '2': prolabore2}

    assert list(prolabores) == [prolabore1, prolabore2]


class TestFetch:
    def test_call_client(self, prolabores):
        year = 2022

        prolabores.fetch(year)

        prolabores.client.prolabores.assert_called_once_with(
            prolabores.company_id,
            year,
        )

    def test_create_prolabores(self, prolabores, prolabores_data):
        prolabores.client.prolabores.return_value = prolabores_data

        prolabores.fetch(2022)

        assert list(prolabores) == [
            Prolabore.from_data(d[0], prolabores.company_id, prolabores.client)
            for d in prolabores_data.values()
        ]

    def test_ignore_empty_competences(self, prolabores):
        prolabores.client.prolabores.return_value = {'2022-07-01': False}

        prolabores.fetch(2022)

        assert list(prolabores) == []

    def test_ignore_empty_prolabore(self, prolabores):
        prolabores.client.prolabores.return_value = {
            '2022-02-01': [{'contraCheque': None}],
        }

        prolabores.fetch(2022)

        assert list(prolabores) == []


class TestGet:
    def test_call_client(self, prolabores, prolabores_data):
        prolabores.client.prolabores.return_value = prolabores_data
        competence = Competence.from_data(list(prolabores_data.keys())[0])

        prolabores.get(competence)

        prolabores.client.prolabores.assert_called_once_with(
            prolabores.company_id,
            competence.year,
        )

    def test_cache(self, prolabores, prolabores_data):
        prolabores.client.prolabores.return_value = prolabores_data
        competence = Competence.from_data(list(prolabores_data.keys())[0])

        prolabores.get(competence)
        prolabores.get(competence)

        prolabores.client.prolabores.assert_called_once()
