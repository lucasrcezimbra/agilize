from uuid import uuid4

import pytest

from agilize import Client
from agilize.agilize import Company


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
