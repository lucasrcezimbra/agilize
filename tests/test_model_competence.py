from datetime import date, datetime

from agilize import Competence


def test_init_convert():
    competence = Competence('2022', '5')
    assert isinstance(competence.year, int)
    assert isinstance(competence.month, int)
    assert Competence('2022', '5') == Competence(2022, 5)


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


def test_from_date():
    assert Competence.from_date(date(2022, 11, 8)) == Competence(2022, 11)
    assert Competence.from_date(datetime(2022, 10, 30)) == Competence(2022, 10)
    assert Competence.from_date(datetime(2022, 9, 30, 8, 32)) == Competence(2022, 9)


def test_str():
    assert str(Competence(2022, 5)) == '202205'
    assert str(Competence(2000, 12)) == '200012'
    assert str(Competence(2123, 1)) == '212301'


def test_first_date():
    assert Competence(2022, 5).first_date == date(2022, 5, 1)
    assert Competence(2000, 12).first_date == date(2000, 12, 1)
    assert Competence(2123, 1).first_date == date(2123, 1, 1)


def test_last_date():
    assert Competence(2022, 5).last_date == date(2022, 5, 31)
    assert Competence(2000, 12).last_date == date(2000, 12, 31)
    assert Competence(2123, 1).last_date == date(2123, 1, 31)
    assert Competence(2022, 2).last_date == date(2022, 2, 28)
    assert Competence(2020, 2).last_date == date(2020, 2, 29)


def test_next():
    assert Competence(2022, 5).next == Competence(2022, 6)
    assert Competence(2022, 12).next == Competence(2023, 1)
    assert Competence(2022, 12).next.next == Competence(2023, 2)
    assert Competence(2021, 1).next == Competence(2021, 2)


def test_previous():
    assert Competence(2022, 5).previous == Competence(2022, 4)
    assert Competence(2022, 12).previous == Competence(2022, 11)
    assert Competence(2022, 12).previous.previous == Competence(2022, 10)
    assert Competence(2021, 1).previous == Competence(2020, 12)
