from uuid import uuid4

import pytest

from agilize.agilize import Competence, Prolabore


@pytest.fixture
def prolabore(faker, client_mock):
    return Prolabore(
        client=client_mock,
        company_id=str(uuid4()),
        competence=Competence(faker.year(), faker.month()),
        inss=faker.pydecimal(),
        irpf=faker.pydecimal(),
        net_value=faker.pydecimal(),
        partner_id=str(uuid4()),
        paycheck_id=str(uuid4()),
        total_value=faker.pydecimal(),
    )


def test_from_data(prolabores_data):
    data = list(prolabores_data.values())[0][0]
    company_id = str(uuid4())
    client = object

    prolabore = Prolabore.from_data(data, company_id, client)

    assert prolabore.client == client
    assert prolabore.company_id == company_id
    assert prolabore.competence == Competence.from_data(data['competence'])
    assert prolabore.inss == data['iNSS']
    assert prolabore.irpf == data['iRPJFolha']
    assert prolabore.net_value == data['valorLiquido']
    assert prolabore.total_value == data['valor']
    assert prolabore.paycheck_id == data['contraCheque']['__identity']


def test_download(prolabore):
    prolabore.download()

    prolabore.client.download_paycheck.assert_called_once_with(
        prolabore.company_id,
        prolabore.partner_id,
        prolabore.competence.year,
        prolabore.competence.month,
    )
