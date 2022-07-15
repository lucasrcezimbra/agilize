from agilize import Company, Competence, Prolabore, Tax


def test_from_data(company_data):
    client = object

    company = Company.from_data(company_data, client)

    assert company.id == company_data['__identity']
    assert company.cnpj == company_data['cnpj']
    assert company.name == company_data['name']
    assert company.client == client


def test_prolabores(company, prolabores_data):
    company.client.prolabores.return_value = prolabores_data
    competence = Competence.from_data(list(prolabores_data.keys())[0])

    prolabore = company.prolabores.get(competence)

    data = list(prolabores_data.values())[0][0]
    assert prolabore == Prolabore(
        client=company.client,
        company_id=company.id,
        competence=Competence.from_data(data['competence']),
        inss=data['iNSS'],
        irpf=data['iRPJFolha'],
        net_value=data['valorLiquido'],
        partner_id=data['partner']['__identity'],
        paycheck_id=data['contraCheque']['__identity'],
        total_value=data['valor'],
    )


def test_taxes(company, taxes_data):
    company.client.taxes.return_value = taxes_data
    competence = Competence.from_data(taxes_data[0]['competence'])

    tax = company.taxes.get(competence)

    data = taxes_data[0]
    assert tax == Tax(
        abbreviation=data['taxAbbreviation'],
        client=company.client,
        company_id=company.id,
        competence=Competence.from_data(data['competence']),
        id=data['__identity'],
    )
