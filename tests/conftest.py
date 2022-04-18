from uuid import uuid4

import pytest


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
