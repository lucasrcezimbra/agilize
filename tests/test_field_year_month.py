from agilize.agilize import YearMonth


def test_from_data(prolabores_data):
    year_month = YearMonth.from_data('2022-04')
    assert year_month.year == 2022
    assert year_month.month == 4

    year_month = YearMonth.from_data('2022-05-10')
    assert year_month.year == 2022
    assert year_month.month == 5

    year_month = YearMonth.from_data("2022-06-01T00:00:00-0300")
    assert year_month.year == 2022
    assert year_month.month == 6
