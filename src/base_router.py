import time
import csv
import random

from datetime import datetime
from loguru import logger
from web3 import Web3

from config.swaps_config import token_arr

from utils import Utils


with open('config/abi_config.txt', 'r') as conf_file:
    abi_lst = [abi for abi in conf_file]

    abi_arb = abi_lst[0]
    abi_rpc = abi_lst[1]
    abi_sushi = abi_lst[2]
    abi_token = abi_lst[3]


class BaseRouter:
    def __init__(self):
        self.RPC = 'https://nova.arbitrum.io/rpc'
        self.GAS = 400000
        self.eth = Web3.to_checksum_address('0x722e8bdd2ce80a4422e880164f2079488e115365')
        self.arb_router = Web3.to_checksum_address('0xee01c0cd76354c383b8c7b4e65ea88d00b06f36f')
        self.sushi_router = Web3.to_checksum_address('0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506')
        self.rpc_router = Web3.to_checksum_address('0x28e0f3ebab59a998c4f1019358388b5e2ca92cfa')
        self.abi_arb = abi_arb
        self.abi_rpc = abi_rpc
        self.abi_sushi = abi_sushi
        self.abi_token = abi_token
        self.token_arr = token_arr
        self.utils = Utils(self.RPC, self.GAS, self.abi_token)

    def swap_buy(self, private_key, token_to_buy, amount, symbol, gas_limit, router, abi):
        """
        Функция для покупки токенов.
        """
        web3 = Web3(Web3.HTTPProvider(self.RPC))  # подключение к ноде через HTTP провайдера
        account = web3.eth.account.from_key(private_key)  # получение аккаунта при помощи приватного ключа
        address_wallet = account.address  # получение адреса аккаунта

        try:
            contract = web3.eth.contract(address=router, abi=abi)  # получение контракта роутера
            # формирование транзакции
            contract_txn = contract.functions.swapExactETHForTokens(
                0,  # amountOutMin
                [self.eth, token_to_buy],  # TokenSold, TokenBuy
                address_wallet,  # receiver
                (int(time.time()) + 10000)  # deadline)
            ).build_transaction({
                'from': address_wallet,
                'value': web3.to_wei(amount, 'ether'),
                'gasPrice': web3.eth.gas_price,
                'gas': self.GAS,
                'nonce': web3.eth.get_transaction_count(address_wallet)
            })

            if self.utils.gas_check(web3, contract_txn['gasPrice'], contract_txn['gas'], gas_limit):
                logger.info('Лимит газа превышен.')
                return True
            else:
                logger.info('Лимит газа не превышен.')

            signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)  # подпись транзакции
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)  # отправка транзакции и получение хеша
            logger.info(f'Buy {symbol} ArbSwap| https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}')
            logger.info(f'    {address_wallet}')

            with open('data/transaction_history.csv', 'w') as transactions_file:
                tnx_writer = csv.writer(transactions_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

                tnx_writer.writerow([private_key, tx_hash, datetime.now(), 'swap', 'ETH Nova', token_to_buy,
                                     web3.to_wei(amount, 'ether')])

        except Exception as error:
            logger.error(f'{symbol} Buy ArbSwap error | {error}')
            logger.error(f'    {address_wallet}')

    def swap_sold(self, private_key, token_to_sold, symbol, gas_limit, router, abi):
        """
        Функция для продажи токенов.
        """
        web3 = Web3(Web3.HTTPProvider(self.RPC))  # подключение к ноде через HTTP провайдера
        account = web3.eth.account.from_key(private_key)  # получение аккаунта при помощи приватного ключа
        address_wallet = account.address  # получение адреса аккаунта

        try:
            contract = web3.eth.contract(address=router, abi=abi)  # получение контракта роутера
            token_sold = web3.eth.contract(address=token_to_sold, abi=self.abi_token)  # получение контракта токена для продажи

            token_balance = token_sold.functions.balanceOf(address_wallet).call()  # получение баланса токена на указанном адресе кошелька

            allowance = self.utils.check_allowance(private_key, token_to_sold, router)  # проверка количества токенов, которые контракт может потратить

            if allowance < 10:
                self.utils.approve(private_key, token_to_sold, router, symbol)  # подтверждение транзакции
                time.sleep(25)

            # формирование транзакции
            contract_txn = contract.functions.swapExactTokensForETH(
                token_balance,
                0,
                [token_to_sold, self.eth],
                address_wallet,
                (int(time.time()) + 100000)
            ).build_transaction({
                'from': address_wallet,
                'gasPrice': web3.eth.gas_price,
                'gas': self.GAS,
                'nonce': web3.eth.get_transaction_count(address_wallet),
            })

            if self.utils.gas_check(web3, contract_txn['gasPrice'], contract_txn['gas'], gas_limit):
                logger.info('Лимит газа превышен.')
                return True
            else:
                logger.info('Лимит газа не превышен.')

            signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)  # подпись транзакции
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)  # отправка транзакции и получение хеша
            logger.info(f'Sold {symbol} ArbSwap | https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}')
            logger.info(f'    {address_wallet}')

            with open('data/transaction_history.csv', 'w') as transactions_file:
                tnx_writer = csv.writer(transactions_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)

                tnx_writer.writerow(
                    [private_key, tx_hash, datetime.now(), 'swap', token_to_sold, 'ETH Nova', token_balance])

        except Exception as error:
            logger.error(f'{symbol} Sold ArbSwap error | {error}')
            logger.error(f'    {address_wallet}')

    def swap(self, private_key, router, abi, amount, token_address, symbol, gas_limit):
        """
        Функция для совершения транзакций (осуществляет покупку и продажу). Биржа выбирается случайно.
        """
        self.swap_buy(private_key, token_address, amount, symbol, gas_limit, router, abi)  # покупка
        time.sleep(random.randint(20, 50))
        self.swap_sold(private_key, token_address, symbol, gas_limit, router, abi)  # продажа
        time.sleep(random.randint(20, 50))
