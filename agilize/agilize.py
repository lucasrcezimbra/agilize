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


@define
class YearMonth:
    year: int
    month: int

    @classmethod
    def from_data(cls, data):
        year, month, *_ = data.split('-')
        return cls(year=int(year), month=int(month))


@define
class Prolabore:
    competence: YearMonth
    inss: Decimal
    irpf: Decimal
    net_value: Decimal
    paycheck_id: str
    total_value: Decimal
    client: Client

    @classmethod
    def from_data(cls, data, client):
        return cls(
            competence=YearMonth.from_data(data['competence']),
            inss=data['iNSS'],
            irpf=data['iRPJFolha'],
            net_value=data['valorLiquido'],
            total_value=data['valor'],
            paycheck_id=data['contraCheque']['__identity'],
            client=client,
        )
