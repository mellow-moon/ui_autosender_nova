import time
import decimal
import random
import csv
import requests

from datetime import datetime
from loguru import logger
from web3 import Web3

from config.orbiter_config import ORBITER_AMOUNT, ORBITER_AMOUNT_STR, ORBITER_MAKER, ORBITER_IDS, DATA


class Orbiter:
    def __init__(self):
        self.from_chain = 'ethereum'
        self.to_chain = 'nova'
        self.ORBITER_AMOUNT = ORBITER_AMOUNT
        self.ORBITER_AMOUNT_STR = ORBITER_AMOUNT_STR
        self.ORBITER_MAKER = ORBITER_MAKER
        self.ORBITER_IDS = ORBITER_IDS
        self.DATA = DATA
        self.COINBASE_URL = 'https://api.coinbase.com/v2/exchange-rates?currency=ETH'

    def orbiter_bridge(self, private_key, amount_from, amount_to, orbiter_bridge_gas_limit, min_amount_bridge=0):
        module_str = f'orbiter_bridge : {self.from_chain} => {self.to_chain}'
        logger.info(module_str)

        try:
            # проверка лимитов от orbiter finance
            min_bridge, max_bridge, fees = self.check_orbiter_limits(self.from_chain, self.to_chain)
            min_bridge = min_bridge + fees

            # получение amount из заданного диапазона
            amount = round(random.uniform(amount_from, amount_to), 8)
            amount_to_bridge = amount

            amount = self.get_orbiter_value(amount_to_bridge, self.to_chain)  # получаем нужный amount

            if (amount > min_bridge) and (amount < max_bridge):

                value = self.int_to_decimal(amount, 18)

                web3 = Web3(Web3.HTTPProvider(self.DATA[self.from_chain]['rpc']))
                account = web3.eth.account.from_key(private_key)
                wallet = account.address
                chain_id = web3.eth.chain_id
                nonce = web3.eth.get_transaction_count(wallet)

                if amount >= min_amount_bridge:

                    contract_txn = {
                        'chainId': chain_id,
                        'nonce': nonce,
                        'from': wallet,
                        'to': '0x80C67432656d59144cEFf962E8fAF8926599bCF8',
                        'value': value,
                        'gas': 0,
                        'gasPrice': 0
                    }

                    # добавление цены газа
                    try:
                        gas_price = web3.eth.gas_price  # запрос цены газа

                        contract_txn['gasPrice'] = int(gas_price * random.uniform(1.05, 1.08))

                    except Exception as error:
                        logger.error(error)

                    # добавление лимита газа
                    try:
                        value = contract_txn['value']
                        contract_txn['value'] = 0
                        pluser = [1.05, 1.07]
                        gas_limit = web3.eth.estimate_gas(contract_txn)
                        contract_txn['gas'] = int(gas_limit * random.uniform(pluser[0], pluser[1]))
                        # logger.info(f"gasLimit : {contract_txn['gas']}")
                    except Exception as error:
                        contract_txn['gas'] = random.randint(2000000, 3000000)
                        logger.info(f"estimate_gas error : {error}. random gasLimit : {contract_txn['gas']}")

                    contract_txn['value'] = value

                    if self.check_gas_limit(web3, contract_txn['gasPrice'], contract_txn['gas'],
                                            orbiter_bridge_gas_limit):
                        logger.error('Превышен лимит газа.')
                        return True

                    # формирование транзакции
                    tx_hash = self.sign_tx(web3, contract_txn, private_key)
                    tx_link = f'{self.DATA[self.from_chain]["scan"]}/{tx_hash}'

                    status = self.check_status_tx(self.from_chain, tx_hash)

                    if status == 1:
                        logger.success(f'{module_str} | {tx_link}')
                        with open('data/transaction_history.csv', 'w') as transactions_file:
                            tnx_writer = csv.writer(transactions_file, delimiter=' ', quotechar='|',
                                                    quoting=csv.QUOTE_MINIMAL)

                            tnx_writer.writerow(
                                [private_key, tx_hash, datetime.now(), 'bridge', 'ETH Mainnet', 'ETH Nova', value])

                    else:
                        logger.error(f'{module_str} | tx is failed | {tx_link}')

                else:
                    logger.error(
                        f"{module_str} : can't bridge : {amount} (amount) < {min_amount_bridge} (min_amount_bridge)")

            else:

                if amount < min_bridge:

                    logger.error(f"{module_str} : can't bridge : {amount} (amount) < {min_bridge} (min_bridge)")

                elif amount > max_bridge:

                    logger.error(f"{module_str} : can't bridge : {amount} (amount) > {max_bridge} (max_bridge)")

        except Exception as error:

            logger.error(f'{module_str} | {error}')

    def sign_tx(self, web3, contract_txn, private_key):
        """
        Функция для подписи транзакции, отправки транзакции и получения хеша.
        """
        signed_tx = web3.eth.account.sign_transaction(contract_txn, private_key)
        raw_tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        tx_hash = web3.to_hex(raw_tx_hash)
        return tx_hash

    def check_status_tx(self, chain, tx_hash):
        """
        Функция для проверки статуса транзакции.
        """
        logger.info(f'{chain} : checking tx_status : {tx_hash}')

        while True:
            try:
                rpc_chain = self.DATA[chain]['rpc']
                web3 = Web3(Web3.HTTPProvider(rpc_chain))
                status_ = web3.eth.get_transaction_receipt(tx_hash)
                status = status_["status"]
                if status in [0, 1]:
                    return status
                time.sleep(1)

            except Exception as error:
                logger.info(f'error, try again : {error}')
                time.sleep(1)

    def get_orbiter_value(self, base_num, chain):
        base_num_dec = decimal.Decimal(str(base_num))
        orbiter_amount_dec = decimal.Decimal(str(self.ORBITER_AMOUNT[chain]))
        difference = base_num_dec - orbiter_amount_dec
        random_offset = decimal.Decimal(str(random.uniform(-0.000000000000001, 0.000000000000001)))
        result_dec = difference + random_offset
        orbiter_str = self.ORBITER_AMOUNT_STR[chain][-4:]
        result_str = '{:.18f}'.format(result_dec.quantize(decimal.Decimal('0.000000000000000001')))
        result_str = result_str[:-4] + orbiter_str

        return decimal.Decimal(result_str)

    def check_orbiter_limits(self, from_chain, to_chain):
        from_maker = self.ORBITER_IDS[from_chain]
        to_maker = self.ORBITER_IDS[to_chain]

        maker_x_maker = f'{from_maker}-{to_maker}'

        for maker in self.ORBITER_MAKER:

            if maker_x_maker == maker:
                min_bridge = self.ORBITER_MAKER[maker]['ETH-ETH']['minPrice']
                max_bridge = self.ORBITER_MAKER[maker]['ETH-ETH']['maxPrice']
                fees = self.ORBITER_MAKER[maker]['ETH-ETH']['tradingFee']

                return min_bridge, max_bridge, fees

    def check_gas_limit(self, web3, gas_price, gas, gas_limit):
        """
        Функция для проверки газа транзакции.
        """
        response = requests.get(self.COINBASE_URL)
        data = response.json()
        eth_price_in_usd = float(data['data']['rates']['USD'])
        print(f'Текущая цена ETH - {eth_price_in_usd} USD.')

        gas_price_for_txn = gas_price * gas
        gas_price_for_txn = web3.from_wei(gas_price_for_txn, 'ether')

        gas_price_for_txn_in_usd = float(gas_price_for_txn) * eth_price_in_usd
        print('Цена газа в USD: {0:0.15f}'.format(gas_price_for_txn_in_usd))
        print('Цена газа в ETH: {0:0.15f}'.format(gas_price_for_txn))

        if gas_price_for_txn_in_usd > gas_limit:
            return True
        else:
            return False

    def int_to_decimal(self, qty, decimal_value):
        return int(qty * int("".join(["1"] + ["0"] * decimal_value)))

    def decimal_to_int(self, qty, decimal_value):
        return qty / int("".join((["1"] + ["0"] * decimal_value)))
