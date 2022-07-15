import sys
from getpass import getpass
from pprint import pprint

from agilize import Client


def get_data(method_name, *args):
    agilize = Client(getpass('CNPJ: '), getpass('Password: '))
    func = getattr(agilize, method_name)
    data = func(*args)
    return data


def main(method_name, *args):
    data = get_data(method_name, *args)
    pprint(data[:2])


if __name__ == '__main__':
    print('Example: python -m contrib.generate_fixture invoices '
          '0e077812-9a7e-4e9a-a674-82f15fc48654 2022')
    method_name, *args = sys.argv[1:]
    main(method_name, *args)
