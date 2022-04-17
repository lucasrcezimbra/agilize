from agilize.agilize import Company


def test_from_data(company_data):
    company = Company.from_data(company_data)

    assert company.id == company_data['__identity']
    assert company.cnpj == company_data['cnpj']
    assert company.name == company_data['name']
