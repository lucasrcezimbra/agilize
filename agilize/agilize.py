from collections import defaultdict
from decimal import Decimal
from typing import Optional

from attrs import define, field

from agilize.client import Client


class Agilize:
    def __init__(self, username, password, client=None):
        self.client = client or Client(username, password)

    def companies(self):
        return [
            Company.from_data(c, self.client)
            for c in self.client.info['party']['companies']
        ]


@define(kw_only=True)
class Prolabores:
    client: Client
    company_id: str
    _prolabores: dict = field(factory=dict)

    def get(self, competence):
        if competence not in self._prolabores:
            self.fetch(competence.year)

        return self._prolabores[competence]

    def fetch(self, year):
        # TODO: implement multiple partners
        data_by_date = self.client.prolabores(self.company_id, year)

        for datas in data_by_date.values():
            if not isinstance(datas, list):
                continue

            for d in datas:
                if not d['contraCheque']:
                    continue

                prolabore = Prolabore.from_data(d, self.company_id, self.client)
                self._prolabores[prolabore.competence] = prolabore

    def __iter__(self):
        yield from self._prolabores.values()


@define(kw_only=True)
class Taxes:
    client: Client
    company_id: str
    _taxes_by_competence: defaultdict = field(factory=lambda: defaultdict(dict))

    def get(self, abbreviation, competence):
        if competence not in self._taxes_by_competence:
            self.fetch(competence.year)

        return self._taxes_by_competence[competence][abbreviation]

    def fetch(self, year):
        data = self.client.taxes(self.company_id, year)

        for d in data:
            tax = Tax.from_data(d, self.company_id, self.client)
            self._taxes_by_competence[tax.competence][tax.abbreviation] = tax

    def filter(self, competence):
        if competence not in self._taxes_by_competence:
            self.fetch(competence.year)

        return list(self._taxes_by_competence[competence].values())

    def __iter__(self):
        for t in self._taxes_by_competence.values():
            yield from t.values()


@define
class Company:
    id: str
    cnpj: str
    name: str
    client: Client
    _prolabores: Optional[Prolabores] = None
    _taxes: Optional[Taxes] = None

    @classmethod
    def from_data(cls, data, client):
        return cls(
            id=data['__identity'],
            cnpj=data['cnpj'],
            name=data['name'],
            client=client,
        )

    @property
    def prolabores(self):
        if not self._prolabores:
            self._prolabores = Prolabores(client=self.client, company_id=self.id)
        return self._prolabores

    @property
    def taxes(self):
        if not self._taxes:
            self._taxes = Taxes(client=self.client, company_id=self.id)
        return self._taxes


@define(hash=True)
class Competence:
    year: int
    month: int

    @classmethod
    def from_data(cls, data):
        year, month, *_ = data.split('-')
        return cls(year=int(year), month=int(month))

    def __str__(self):
        return f'{self.year:04d}{self.month:02d}'


@define
class Prolabore:
    client: Client
    company_id: str
    competence: Competence
    inss: Decimal
    irpf: Decimal
    net_value: Decimal
    partner_id: str
    paycheck_id: str
    total_value: Decimal

    @classmethod
    def from_data(cls, data, company_id, client):
        return cls(
            client=client,
            company_id=company_id,
            competence=Competence.from_data(data['competence']),
            inss=data['iNSS'],
            irpf=data['iRPJFolha'],
            net_value=data['valorLiquido'],
            partner_id=data['partner']['__identity'],
            paycheck_id=data['contraCheque']['__identity'],
            total_value=data['valor'],
        )

    def download(self):
        return self.client.download_prolabore(
            self.company_id,
            self.partner_id,
            self.competence.year,
            self.competence.month,
        )


@define
class Tax:
    client: Client
    abbreviation: str
    company_id: str
    competence: Competence
    id: str

    @classmethod
    def from_data(cls, data, company_id, client):
        return cls(
            abbreviation=data['taxAbbreviation'],
            client=client,
            company_id=company_id,
            competence=Competence.from_data(data['competence']),
            id=data['__identity'],
        )

    def download(self):
        return self.client.download_tax(self.company_id, self.id)
