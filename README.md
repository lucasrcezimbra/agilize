# Agilize

[![PyPI](https://badge.fury.io/py/Agilize.svg)](https://badge.fury.io/py/Agilize)
[![Coverage Status](https://coveralls.io/repos/github/lucasrcezimbra/agilize/badge.svg?branch=master)](https://coveralls.io/github/lucasrcezimbra/agilize?branch=master)

Unofficial client to access [Agilize](https://www.agilize.com.br/).


## Installation

```bash
pip install agilize
```


## How to Use

High-level API

```python
from agilize import Agilize


agilize = Agilize(username='11222333000160', password='p4ssw0rd')


companies = agilize.companies()

for company in companies:
    print(company)


company = companies[0]

for prolabore in company.prolabores(year=2022):
    print(prolabore)
```

Low-level API

```python
from agilize import Client


agilize = Client(username='11222333000160', password='p4ssw0rd')

print(agilize.info)
company_id = agilize.info['party']['companies'][0]['__identity']

agilize.prolabores(company_id=company_id, year=2022)
```



## Contributing
Contributions are welcome, feel free to open an Issue or Pull Request.

Pull requests must be for the `develop` branch.

```bash
git clone https://github.com/lucasrcezimbra/agilize
cd agilize
git checkout develop
python -m venv .venv
pip install -r requirements-dev.txt
pre-commit install
pytest
```
