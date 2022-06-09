from decimal import Decimal

from attrs import define

from agilize.client import Client


class Agilize:
    def __init__(self, username, password, client=None):
        self.client = client or Client(username, password)

    def companies(self):
        return [
            Company.from_data(c, self.client)
            for c in self.client.info['party']['companies']
        ]


@define
class Company:
    id: str
    cnpj: str
    name: str
    client: Client

    @classmethod
    def from_data(cls, data, client):
        return cls(
            id=data['__identity'],
            cnpj=data['cnpj'],
            name=data['name'],
            client=client,
        )

    def prolabores(self, year):
        # TODO: create class Prolabores
        prolabores = []
        prolabores_data_by_date = self.client.prolabores(self.id, year)

        for prolabores_data in prolabores_data_by_date.values():
            if not isinstance(prolabores_data, list):
                continue

            for data in prolabores_data:
                if not data['contraCheque']:
                    continue
                prolabores.append(Prolabore.from_data(data, self))

        return prolabores


@define
class Competence:
    year: int
    month: int

    @classmethod
    def from_data(cls, data):
        year, month, *_ = data.split('-')
        return cls(year=int(year), month=int(month))


@define
class Prolabore:
    client: Client
    company: Company
    competence: Competence
    inss: Decimal
    irpf: Decimal
    net_value: Decimal
    partner_id: str
    paycheck_id: str
    total_value: Decimal

    @classmethod
    def from_data(cls, data, company):
        return cls(
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

    def download(self):
        return self.client.download_paycheck(
            self.company.id,
            self.partner_id,
            self.competence.year,
            self.competence.month,
        )
