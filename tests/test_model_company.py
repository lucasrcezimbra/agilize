from uuid import uuid4

import pytest

from agilize import Client
from agilize.agilize import Company, Competence, Prolabore


@pytest.fixture
def company(faker, mocker):
    return Company(
        id=str(uuid4()),
        cnpj='',
        name=faker.company(),
        client=mocker.create_autospec(Client)
    )


def test_from_data(company_data):
    client = object

    company = Company.from_data(company_data, client)

    assert company.id == company_data['__identity']
    assert company.cnpj == company_data['cnpj']
    assert company.name == company_data['name']
    assert company.client == client


def test_prolabores(company, prolabores_data):
    company.client.prolabores.return_value = prolabores_data

    prolabores = company.prolabores(2022)

    data = list(prolabores_data.values())
    first = data[0][0]
    second = data[1][0]
    assert len(prolabores) == 2
    assert prolabores[0] == Prolabore(
        client=company.client,
        competence=Competence.from_data(first['competence']),
        inss=first['iNSS'],
        irpf=first['iRPJFolha'],
        net_value=first['valorLiquido'],
        paycheck_id=first['contraCheque']['__identity'],
        total_value=first['valor'],
    )
    assert prolabores[1] == Prolabore(
        client=company.client,
        competence=Competence.from_data(second['competence']),
        inss=second['iNSS'],
        irpf=second['iRPJFolha'],
        net_value=second['valorLiquido'],
        paycheck_id=second['contraCheque']['__identity'],
        total_value=second['valor'],
    )


def test_prolabores_filter_out_data_false(company, prolabores_data):
    prolabores_data['2022-07-01'] = False
    company.client.prolabores.return_value = prolabores_data

    prolabores = company.prolabores(2022)

    assert len(prolabores) == 2


def test_prolabores_filter_out_without_paycheck(company, prolabores_data):
    prolabores_data['2022-02-01'][0]['contraCheque'] = None
    company.client.prolabores.return_value = prolabores_data

    prolabores = company.prolabores(2022)

    assert len(prolabores) == 1
