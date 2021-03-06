from agilize import Competence


def test_from_data():
    c1 = Competence.from_data('2022-05-01')
    assert c1.year == 2022
    assert c1.month == 5

    c2 = Competence.from_data('2021-04-25T11:14:53.416030')
    assert c2.year == 2021
    assert c2.month == 4

    c3 = Competence.from_data('2000-12-32')
    assert c3.year == 2000
    assert c3.month == 12


def test_str():
    assert str(Competence(2022, 5)) == '202205'
    assert str(Competence(2000, 12)) == '200012'
    assert str(Competence(2123, 1)) == '212301'
