from agilize.agilize import Competence


def test_from_data(prolabores_data):
    competence = Competence.from_data('2022-04')
    assert competence.year == 2022
    assert competence.month == 4

    competence = Competence.from_data('2022-05-10')
    assert competence.year == 2022
    assert competence.month == 5

    competence = Competence.from_data("2022-06-01T00:00:00-0300")
    assert competence.year == 2022
    assert competence.month == 6
