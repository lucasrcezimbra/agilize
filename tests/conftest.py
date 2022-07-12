import random
from uuid import uuid4

import pytest
from faker.providers.python import Provider as PythonProvider

from agilize import Client, Company


class Provider(PythonProvider):
    def money(self, negative=False):
        return self.pyfloat(
            left_digits=random.randint(3, 4),
            right_digits=2,
            positive=(not negative),
        )


@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['pt_BR']


@pytest.fixture(autouse=True)
def faker(faker):
    faker.add_provider(Provider)
    return faker


@pytest.fixture
def client_mock(mocker):
    return mocker.create_autospec(Client)


@pytest.fixture
def company(faker, client_mock):
    return Company(
        id=str(uuid4()),
        cnpj='',
        name=faker.company(),
        client=client_mock,
    )


@pytest.fixture
def info_data(faker):
    return {
        'accountIdentifier': '12345678000160',
        'creationDate': '2022-04-17T17:11:00-0300',
        'expirationDate': None,
        'party': {
            'companies': [
                {
                    'activityType': 1,
                    'city': {'code': '1234567', 'name': 'Porto Alegre'},
                    'clientSince': '2022-04-17T17:11:00-0300',
                    'cnpj': '12345678000160',
                    'email': faker.email(),
                    'firstEmail': faker.email(),
                    'foundingDate': '2022-04-17T17:13:00-0300',
                    'hasEmployees': False,
                    'hasFinanceiro': True,
                    'isAgilizePremium': False,
                    'isBlocked': False,
                    'isComercio': False,
                    'isHabilitadoEmitirNfse': False,
                    'isLucroPresumido': False,
                    'isMei': False,
                    'isOperadoPorProcuracao': False,
                    'lockedAt': None,
                    'name': faker.company(),
                    '__identity': str(uuid4()),
                }
            ],
            'email': faker.email(),
            'emailIsVerified': True,
            'name': None,
            'temporaryEmail': None,
            '__identity': str(uuid4()),
        },
        'roles': {
            'Agilize.Api:Customer': {
                'identifier': 'Agilize.Api:Customer',
                'name': 'Customer',
            }
        },
    }


@pytest.fixture
def company_data(info_data):
    return info_data['party']['companies'][0]


@pytest.fixture
def partners_data(faker):
    return [
        {
            "amountOfDependent": faker.pyint(),
            "birthDate": "1900-09-03T00:00:00-0300",
            "company": {"isAutomaticFatorR": faker.pybool()},
            "currentProlabore": faker.pyint(),
            "hasIncompleteDataForEsocial": faker.pybool(),
            "hasUnregisteredDependent": faker.pybool(),
            "isAdmin": faker.pybool(),
            "isSeniorPartner": faker.pybool(),
            "mainDocument": "01234567890",
            "name": faker.name(),
            "person": {
                "birthDate": "1900-09-03T00:00:00-0300",
                "certificatesA3": [],
                "cityOfBirth": {
                    "__isInitialized__": faker.pybool(),
                    "agilizeEnabled": faker.pybool(),
                    "code": "1234567",
                    "codigoSIAFI": "1234",
                    "dddCode": "55",
                    "name": "Porto Alegre",
                    "slugName": "porto_alegre",
                    "timezone": None,
                    "__identity": str(uuid4()),
                },
                "countryOfBirth": None,
                "countryOfNationality": None,
                "cpf": "01234567890",
                "defaultAddress": {
                    "addressType": None,
                    "area": None,
                    "city": {
                        "__isInitialized__": faker.pybool(),
                        "agilizeEnabled": faker.pybool(),
                        "code": "1234567",
                        "codigoSIAFI": "1234",
                        "dddCode": "55",
                        "name": "Porto Alegre",
                        "slugName": "porto_alegre",
                        "timezone": None,
                        "__identity": str(uuid4()),
                    },
                    "cityCode": "1234567",
                    "cityName": "Porto Alegre",
                    "complement": "house 1",
                    "formattedAddress": "Rua A, 123,Complemento: house 1",
                    "formattedForProlabore": "Rua A, 123,Complemento: house 1",
                    "invalid": faker.pybool(),
                    "invalidReason": None,
                    "iptu": None,
                    "isDefault": faker.pybool(),
                    "neighborhood": "São Paulo",
                    "number": "123",
                    "originalPlainText": None,
                    "semNumero": faker.pybool(),
                    "state": {
                        "__isInitialized__": faker.pybool(),
                        "abbreviation": "RS",
                        "code": "12",
                        "name": "Rio Grande do Sul",
                        "__identity": str(uuid4()),
                    },
                    "stateAbbreviation": "RS",
                    "street": "Rua A",
                    "zipCode": "90000000",
                    "Flow_Persistence_clone": faker.pybool(),
                    "__identity": str(uuid4()),
                },
                "dependencias": [],
                "documents": [
                    {
                        "documentNumber": "12345678910",
                        "documentType": {
                            "__isInitialized__": faker.pybool(),
                            "abbreviation": "PIS",
                            "identification": faker.pybool(),
                            "mask": None,
                            "personType": 1,
                            "slugname": "pispasep",
                            "__identity": str(uuid4()),
                        },
                        "__identity": str(uuid4()),
                    }
                ],
                "foreignAddress": None,
                "foreignRegisterExpedition": None,
                "foreignRegisterNumber": "",
                "foreignRegisterOrganizationEmmit": "",
                "gender": faker.pyint(),
                "hasChildrenWithBrazilian": None,
                "hasForeignRegister": None,
                "isVerificadoNaRfb": faker.pybool(),
                "marriedWithBrazilian": None,
                "name": faker.name(),
                "origin": 1,
                "pisPasep": "12345678910",
                "relationWithBrazil": None,
                "stateOfBirth": {
                    "__isInitialized__": faker.pybool(),
                    "abbreviation": "RS",
                    "code": "12",
                    "name": "Rio Grande do Sul",
                    "__identity": str(uuid4()),
                },
                "verificadoNaRfb": faker.pybool(),
                "__meta": {"isPartnerDataComplete": faker.pybool()},
                "__identity": str(uuid4()),
            },
            "salaryAmount": 0,
            "share": faker.pyint(),
            "updatedAt": "2022-04-17T21:56:00-0300",
            "__identity": str(uuid4()),
        }
    ]


@pytest.fixture
def prolabores_data(faker):
    return {
        "2022-02-01": [
            {
                "amountOfDependent": 0,
                "competence": "2022-02-01T00:00:00-0300",
                "contraCheque": {"__identity": str(uuid4())},
                "deducaoDependente": 0,
                "iNSS": faker.money(),
                "iNSSBrl": str(faker.money()),
                "iNSSPatronal": 0,
                "iNSSPatronalBrl": "0,00",
                "iNSSTotal": faker.money(),
                "iNSSTotalBrl": str(faker.money()),
                "iRPJFolha": 0,
                "iRPJFolhaBrl": "0,00",
                "iRRF": False,
                "iRRFAliquota": 0,
                "iRRFAliquotaAsPercent": 0,
                "iRRFBase": faker.money(),
                "isAnexoIV": False,
                "isLucroPresumido": False,
                "isSimplesNacional": True,
                "pagamentoProlabore": None,
                "partner": {"__identity": str(uuid4())},
                "partnerName": faker.name(),
                "provisaoINSSPatronal": None,
                "rubricasDescontos": [],
                "rubricasProventos": [],
                "salaryAmount": 0,
                "saldoInssAPagarAposCompensacoes": faker.money(),
                "totalCompensacoes": 0,
                "totalDeImpostos": faker.money(),
                "valor": faker.pyint(),
                "valorBrl": str(faker.money()),
                "valorLiquido": faker.money(),
                "valorLiquidoBrl": str(faker.money()),
                "valorTotalDescontos": 0,
                "valorTotalProventos": 0,
            }
        ],
        "2022-01-01": [
            {
                "amountOfDependent": 0,
                "competence": "2022-01-01T00:00:00-0300",
                "contraCheque": {"__identity": str(uuid4())},
                "deducaoDependente": 0,
                "iNSS": faker.money(),
                "iNSSBrl": str(faker.money()),
                "iNSSPatronal": 0,
                "iNSSPatronalBrl": "0,00",
                "iNSSTotal": faker.money(),
                "iNSSTotalBrl": str(faker.money()),
                "iRPJFolha": 0,
                "iRPJFolhaBrl": "0,00",
                "iRRF": False,
                "iRRFAliquota": 0,
                "iRRFAliquotaAsPercent": 0,
                "iRRFBase": faker.money(),
                "isAnexoIV": False,
                "isLucroPresumido": False,
                "isSimplesNacional": True,
                "pagamentoProlabore": None,
                "partner": {"__identity": str(uuid4())},
                "partnerName": faker.name(),
                "provisaoINSSPatronal": None,
                "rubricasDescontos": [],
                "rubricasProventos": [],
                "salaryAmount": 0,
                "saldoInssAPagarAposCompensacoes": faker.money(),
                "totalCompensacoes": 0,
                "totalDeImpostos": faker.money(),
                "valor": faker.pyint(),
                "valorBrl": str(faker.money()),
                "valorLiquido": faker.money(),
                "valorLiquidoBrl": str(faker.money()),
                "valorTotalDescontos": 0,
                "valorTotalProventos": 0,
            }
        ],
    }


@pytest.fixture
def taxes_data(faker):
    return [
        {
            'automaticAuditErrorCode': '500',
            'billet': {'__identity': str(uuid4())},
            'billetLastUpdate': '2022-07-03T12:34:56-0300',
            'closed': faker.pybool(),
            'competence': '2022-06-01T00:00:00-0300',
            'competenceIntervalDate': {
                'from': '2022-06-01T00:00:00-0300',
                'to': '2022-06-30T23:59:59-0300',
            },
            'createdBy': None,
            'deadline': '2022-07-20T23:59:59-0300',
            'dueTax': faker.money(),
            'dueTaxLessThanMinValue': faker.pybool(),
            'evidence': None,
            'evidenceLastUpdate': None,
            'finalPaid': faker.pybool(),
            'hasCertified': None,
            'hasHonorarioSucumbencia': faker.pybool(),
            'interest': None,
            'isAutomaticRecalculation': faker.pybool(),
            'lastRecalculationAt': None,
            'manuallyCreatedReason': None,
            'needRecalculation': faker.pybool(),
            'newDeadlineRequest': None,
            'officialDueValue': faker.money(),
            'officialEvidences': [],
            'paid': faker.pybool(),
            'paidAt': None,
            'penalties': None,
            'periodRevenue': faker.money(),
            'recalculation': faker.pybool(),
            'releasedToClient': faker.pybool(),
            'retention': 0,
            'showTax': faker.pybool(),
            'status': 1,
            'tax': {
                'abbreviation': 'DAS',
                'disabledAt': None,
                'friendlyName': None,
                'name': 'Documento de Arrecadação do Simples Nacional',
                'slugName': 'DAS',
                'taxType': 3,
                '__identity': str(uuid4()),
            },
            'taxAbbreviation': 'DAS',
            'taxMinValueToPay': 10,
            'taxSlugName': 'DAS',
            'taxWillAggregatePayment': None,
            'total': faker.money(),
            'underReview': faker.pybool(),
            'updatedAt': '2022-07-02T13:48:19-0300',
            'valorFaturamento': 0,
            'valorImposto': faker.money(),
            'valorImpostos': faker.money(),
            'valorRetencoes': 0,
            'wasManuallyCreated': faker.pybool(),
            '__identity': str(uuid4()),
        },
    ]
