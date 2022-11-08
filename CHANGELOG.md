# Changelog


## 0.0.7 (2022-11-08)
- Add Action to publish on PyPI [#1](https://github.com/lucasrcezimbra/agilize/issues/1)
- Fix Prolabore.from_data to cast values to Decimal
- Improve Competence adding `previous`, `next`, `last_date`, `from_date`, `first_date`
- Update dev requirements


## 0.0.6 (2022-10-29)
- Enable NFSE upload - Agilize.upload_nfse and Client.upload_nfse
- Update dev requirements


## 0.0.5 (2022-07-23)
- Download invoices NFSE
- Update dev dependencies
  * faker 13.15.0 ~> 13.15.1


## 0.0.4 (2022-07-15)
- BREAKING CHANGE: Rename Client.download_paycheck to download_prolabore
- BREAKING CHANGE: Update Client.PATH_*
- Add taxes with download
- Add Client.invoices
- Add script to help fixture generation
- Update dev dependencies
  * faker 13.14.0 ~> 13.15.0
  * pre-commit 2.19.0 ~> 2.20.0
  * pytest-mock 3.8.1 ~> 3.8.2


## 0.0.3 (2022-06-25)
- Add pro-labore download
  * add Client.download_paycheck
- Create high-level API
- Update requirements-dev


## 0.0.2 (2022-04-17)
- First version - authentication and prolabores
