import sys

from web3 import Web3


def check_transaction_by_hash(tx_hash):
    print('Проверка хеша транзакции...\n')

    RPC_NOVA = 'https://nova.arbitrum.io/rpc'
    web3 = Web3(Web3.HTTPProvider(RPC_NOVA))

    status_ = web3.eth.get_transaction_receipt(tx_hash)
    status = status_['status']

    if status in [0, 1]:
        res = 'Транзакция проведена успешно.' if status == 1 else 'Транзакция не была проведена.'
        print(res)


try:
    check_transaction_by_hash(sys.argv[1])
except IndexError:
    print('Введите в текстовое поле хеш транзакции!')
except ValueError:
    print('Введено некорректное значение хеша!')
