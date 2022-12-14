from decimal import Decimal

from agilize import Company, Competence, Invoice, Prolabore, Tax


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
        inss=Decimal(str(data['iNSS'])),
        irpf=Decimal(str(data['iRPJFolha'])),
        net_value=Decimal(str(data['valorLiquido'])),
        partner_id=data['partner']['__identity'],
        paycheck_id=data['contraCheque']['__identity'],
        total_value=Decimal(str(data['valor'])),
    )


def test_taxes(company, taxes_data):
    company.client.taxes.return_value = taxes_data
    abbreviation = taxes_data[0]['taxAbbreviation']
    competence = Competence.from_data(taxes_data[0]['competence'])

    tax = company.taxes.get(abbreviation, competence)

    data = taxes_data[0]
    assert tax == Tax(
        abbreviation=data['taxAbbreviation'],
        client=company.client,
        company_id=company.id,
        competence=Competence.from_data(data['competence']),
        id=data['__identity'],
    )


def test_invoices(company, invoices_data):
    company.client.invoices.return_value = invoices_data
    data = invoices_data[0]
    competence = Competence.from_data(data['competence'])

    invoice = company.invoices.get(competence)

    assert invoice == Invoice.from_data(data)


def test_upload_nfse(company):
    count = 1
    company.client.upload_nfse.return_value = {
        'countNfses': count,
        'createdAt': '2022-10-29T14:40:00-0300',
        'nfses': [],
    }

    assert company.upload_nfse(b'') == count
