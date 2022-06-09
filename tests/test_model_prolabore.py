from uuid import uuid4

import pytest

from agilize import Client
from agilize.agilize import Competence, Prolabore


@pytest.fixture
def prolabore(company, faker, mocker):
    return Prolabore(
        competence=Competence(faker.year(), faker.month()),
        inss=faker.pydecimal(),
        irpf=faker.pydecimal(),
        net_value=faker.pydecimal(),
        partner_id=str(uuid4()),
        paycheck_id=str(uuid4()),
        total_value=faker.pydecimal(),
        company=company,
        client=mocker.create_autospec(Client)
    )


def test_from_data(company, prolabores_data):
    data = list(prolabores_data.values())[0][0]

    prolabore = Prolabore.from_data(data, company)

    assert prolabore.client == company.client
    assert prolabore.company == company
    assert prolabore.competence == Competence.from_data(data['competence'])
    assert prolabore.inss == data['iNSS']
    assert prolabore.irpf == data['iRPJFolha']
    assert prolabore.net_value == data['valorLiquido']
    assert prolabore.total_value == data['valor']
    assert prolabore.paycheck_id == data['contraCheque']['__identity']


def test_download(prolabore):
    prolabore.download()

    prolabore.client.download_paycheck.assert_called_once_with(
        prolabore.company.id,
        prolabore.partner_id,
        prolabore.competence.year,
        prolabore.competence.month,
    )
