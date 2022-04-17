# Agilize

Unofficial client to access [Agilize](https://www.agilize.com.br/).


## Installation

```bash
pip install agilize
```


## How to Use
~~~~~~~~~~~~~
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

.. code-block:: bash

```bash
git clone https://github.com/lucasrcezimbra/agilize
cd agilize
git checkout develop
python -m venv .venv
pip install -r requirements-dev.txt
pre-commit install
pytest
```
