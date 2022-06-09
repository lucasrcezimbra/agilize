from agilize.agilize import Company, Competence, Prolabore


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

    assert len(prolabores) == 2
    data = list(prolabores_data.values())[0][0]
    assert prolabores[0] == Prolabore(
        client=company.client,
        company=company,
        competence=Competence.from_data(data['competence']),
        inss=data['iNSS'],
        irpf=data['iRPJFolha'],
        net_value=data['valorLiquido'],
        partner_id=data['partner']['__identity'],
        paycheck_id=data['contraCheque']['__identity'],
        total_value=data['valor'],
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
