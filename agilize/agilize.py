from attrs import define

from agilize.client import Client


class Agilize:
    def __init__(self, username, password, client=None):
        self.client = client or Client(username, password)

    def companies(self):
        return [Company.from_data(c) for c in self.client.info['party']['companies']]


@define
class Company:
    id: str
    cnpj: str
    name: str

    @classmethod
    def from_data(cls, data):
        return cls(
            id=data['__identity'],
            cnpj=data['cnpj'],
            name=data['name'],
        )
