import requests
import time

from loguru import logger
from web3 import Web3


class Utils:
    def __init__(self, rpc, gas, abi_token):
        self.RPC = rpc
        self.GAS = gas
        self.abi_token = abi_token
        self.COINBASE_URL = 'https://api.coinbase.com/v2/exchange-rates?currency=ETH'

    def add_liquidity(self, private_key, token_to_buy, amount, symbol, router, abi):
        """
        Функция для добавления ликвидности.
        """
        web3 = Web3(Web3.HTTPProvider(self.RPC))
        account = web3.eth.account.from_key(private_key)
        address_wallet = account.address

        try:

            contract = web3.eth.contract(address=router, abi=abi)

            allowance = self.check_allowance(private_key, token_to_buy, router)

            if allowance < 10:
                self.approve(private_key, token_to_buy, router, symbol)
                time.sleep(25)

            amount_ = Web3.to_wei(amount, 'ether')
            contract_txn = contract.functions.addLiquidityETH(
                token_to_buy,
                amount_,
                0,
                0,
                address_wallet,
                (int(time.time()) + 10000)
            ).build_transaction({
                'from': address_wallet,
                'gasPrice': web3.eth.gas_price,
                'gas': self.GAS,
                'value': amount_,
                'nonce': web3.eth.get_transaction_count(address_wallet)
            })

            signed_txn = web3.eth.account.sign_transaction(contract_txn, private_key=private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

            logger.info(f'add liquidity {symbol} | https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}')
            logger.info(f'    {address_wallet}')

        except Exception as error:
            logger.error(f'add liquidity {symbol} error | {error}')
            logger.error(f'    {address_wallet}')

    def check_allowance(self, private_key, token_to_buy, router):
        """
        Функция для получения количества токенов, которые контракт может потратить.
        """
        web3 = Web3(Web3.HTTPProvider(self.RPC))

        account = web3.eth.account.from_key(private_key)
        address_wallet = account.address

        token_contract = web3.eth.contract(address=token_to_buy, abi=self.abi_token)

        allowance = Web3.from_wei(token_contract.functions.allowance(address_wallet, router).call(), 'ether')

        return allowance

    def approve(self, private_key, token_to_approve, address_to_approve, symbol):
        """
        Функция для подтверждения транзакции.
        """
        web3 = Web3(Web3.HTTPProvider(self.RPC))
        account = web3.eth.account.from_key(private_key)
        address_wallet = account.address
        token_contract = web3.eth.contract(address=token_to_approve, abi=self.abi_token)
        max_amount = web3.to_wei(2 ** 32 - 1, 'ether')

        try:
            tx = token_contract.functions.approve(address_to_approve, max_amount).build_transaction({
                'from': address_wallet,
                'gasPrice': web3.eth.gas_price,
                'gas': self.GAS,
                'nonce': web3.eth.get_transaction_count(address_wallet)
            })
            signed_tx = web3.eth.account.sign_transaction(tx, private_key)
            tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

            logger.info(f'{symbol} approve : https://nova.arbiscan.io/tx/{web3.to_hex(tx_hash)}')
            logger.info(f'    {address_wallet}')

        except Exception as error:
            logger.error(f'{symbol} approve error | {error}')
            logger.error(f'    {address_wallet}')

    def gas_check(self, web3, gas_price, gas, gas_limit):
        """
        Функция для проверки газа.
        """
        response = requests.get(self.COINBASE_URL)
        data = response.json()
        eth_price_in_usd = float(data['data']['rates']['USD'])
        print(f'Текущая цена ETH - {eth_price_in_usd} USD.')

        # расчет газа
        gas_price_for_txn = gas_price * gas
        gas_price_for_txn = web3.from_wei(gas_price_for_txn, 'ether')

        # цена газа в usd
        gas_price_for_txn_in_usd = float(gas_price_for_txn) * eth_price_in_usd
        print('Цена газа в USD: {0:0.15f}'.format(gas_price_for_txn_in_usd))
        print('Цена газа в ETH: {0:0.15f}'.format(gas_price_for_txn))
        print('Заданный лимит газа в USD: {0:0.15f}'.format(gas_limit))

        if gas_price_for_txn_in_usd > gas_limit:
            return True
        else:
            return False
