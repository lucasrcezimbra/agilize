from agilize.agilize import Prolabore, YearMonth


def test_from_data(prolabores_data):
    client = object
    data = list(prolabores_data.values())[0][0]

    prolabore = Prolabore.from_data(data, client)

    assert prolabore.client == client
    assert prolabore.competence == YearMonth.from_data(data['competence'])
    assert prolabore.inss == data['iNSS']
    assert prolabore.irpf == data['iRPJFolha']
    assert prolabore.net_value == data['valorLiquido']
    assert prolabore.total_value == data['valor']
    assert prolabore.paycheck_id == data['contraCheque']['__identity']
