import requests
import random


class ArgumentsHandler:
    def __init__(self,
                 orbiter_bridge_checked,
                 abrswap_checked,
                 rpcswap_checked,
                 sushiswap_checked,
                 orbiter_bridge_limit_min,
                 orbiter_bridge_limit_max,
                 arbswap_limit_min,
                 arbswap_limit_max,
                 rpcswap_limit_min,
                 rpcswap_limit_max,
                 sushiswap_limit_min,
                 sushiswap_limit_max,
                 projects_delay_min,
                 projects_delay_max,
                 wallets_delay_min,
                 wallets_delay_max,
                 transactions_count,
                 orbiter_bridge_gas_limit,
                 arbswap_gas_limit,
                 rpcswap_gas_limit,
                 sushiswap_gas_limit):

        # выбранные проекты
        self.orbiter_bridge_checked = True if int(orbiter_bridge_checked) == 2 else False
        self.abrswap_checked = True if int(abrswap_checked) == 2 else False
        self.rpcswap_checked = True if int(rpcswap_checked) == 2 else False
        self.sushiswap_checked = True if int(sushiswap_checked) == 2 else False

        # лимиты в USD
        self.orbiter_bridge_limit_min = float(orbiter_bridge_limit_min)
        self.orbiter_bridge_limit_max = float(orbiter_bridge_limit_max)

        self.arbswap_limit_min = float(arbswap_limit_min)
        self.arbswap_limit_max = float(arbswap_limit_max)

        self.rpcswap_limit_min = float(rpcswap_limit_min)
        self.rpcswap_limit_max = float(rpcswap_limit_max)

        self.sushiswap_limit_min = float(sushiswap_limit_min)
        self.sushiswap_limit_max = float(sushiswap_limit_max)

        # задержки между проектами
        self.projects_delay_min = int(projects_delay_min)
        self.projects_delay_max = int(projects_delay_max)

        # задержки между кошельками
        self.wallets_delay_min = int(wallets_delay_min)
        self.wallets_delay_max = int(wallets_delay_max)

        # нужное количество транзакций
        self.transaction_count = int(transactions_count)

        # лимимты газа в USD
        self.orbiter_bridge_gas_limit = float(orbiter_bridge_gas_limit)
        self.arbswap_gas_limit = float(arbswap_gas_limit)
        self.rpcswap_gas_limit = float(rpcswap_gas_limit)
        self.sushiswap_gas_limit = float(sushiswap_gas_limit)

        self.COINBASE_URL = 'https://api.coinbase.com/v2/exchange-rates?currency=ETH'

        self.checked_projects = []

        # лимиты в ETH
        self.orbiter_bridge_limit_min_eth, \
        self.orbiter_bridge_limit_max_eth, \
        self.arbswap_limit_min_eth, \
        self.arbswap_limit_max_eth, \
        self.rpcswap_limit_min_eth, \
        self.rpcswap_limit_max_eth, \
        self.sushiswap_limit_min_eth, \
        self.sushiswap_limit_max_eth = self.calc_limits_in_eth()

        # лимиты газа в ETH
        self.orbiter_bridge_gas_limit_eth, \
        self.arbswap_gas_limit_eth, \
        self.rpcswap_gas_limit_eth, \
        self.sushiswap_gas_limit_eth = self.calc_gas_limits_in_eth()

        # путь до файла с приватными ключами
        self.private_keys_path = 'data/private_keys.txt'

        self.show_info()

    def calc_limits_in_eth(self):
        eth_price_in_usd = self.get_current_eth_price()

        orbiter_bridge_limit_min_eth = self.orbiter_bridge_limit_min / eth_price_in_usd
        orbiter_bridge_limit_max_eth = self.orbiter_bridge_limit_max / eth_price_in_usd

        arbswap_limit_min_eth = self.arbswap_limit_min / eth_price_in_usd
        arbswap_limit_max_eth = self.arbswap_limit_max / eth_price_in_usd

        rpcswap_limit_min_eth = self.rpcswap_limit_min / eth_price_in_usd
        rpcswap_limit_max_eth = self.rpcswap_limit_max / eth_price_in_usd

        sushiswap_limit_min_eth = self.sushiswap_limit_min / eth_price_in_usd
        sushiswap_limit_max_eth = self.sushiswap_limit_max / eth_price_in_usd

        return orbiter_bridge_limit_min_eth, orbiter_bridge_limit_max_eth, \
               arbswap_limit_min_eth, arbswap_limit_max_eth, \
               rpcswap_limit_min_eth, rpcswap_limit_max_eth, \
               sushiswap_limit_min_eth, sushiswap_limit_max_eth

    def calc_gas_limits_in_eth(self):
        eth_price_in_usd = self.get_current_eth_price()

        orbiter_bridge_gas_limit_eth = self.orbiter_bridge_gas_limit / eth_price_in_usd

        arbswap_gas_limit_eth = self.arbswap_gas_limit / eth_price_in_usd

        rpcswap_gas_limit_eth = self.rpcswap_gas_limit / eth_price_in_usd

        sushiswap_gas_limit_eth = self.sushiswap_gas_limit / eth_price_in_usd

        return orbiter_bridge_gas_limit_eth, arbswap_gas_limit_eth, rpcswap_gas_limit_eth, sushiswap_gas_limit_eth

    def get_current_eth_price(self):
        response = requests.get(self.COINBASE_URL)
        data = response.json()

        current_eth_price = float(data['data']['rates']['USD'])

        return current_eth_price

    def show_info(self):
        print('Запущен скрипт совершения транзакций...')
        print('########################################')

        if self.orbiter_bridge_checked:
            print('Бридж в Orbiter Finance: да.')
            print(f'Максимальный газ при бридже в Orbiter Finance (USD): {self.orbiter_bridge_gas_limit}')
            print(f'Максимальный газ при бридже в Orbiter Finance (ETH): {self.orbiter_bridge_gas_limit_eth}')
            print('########################################')
        else:
            print('Бридж в Orbiter Finance: нет.')
            print('########################################')

        if self.abrswap_checked:
            self.checked_projects.append('arb')
            print('Свап в Arbswap: да.')
            print(f'Максимальный газ при свапе в Arbswap (USD): {self.arbswap_gas_limit}')
            print(f'Максимальный газ при свапе в Arbswap (ETH): {self.arbswap_gas_limit_eth}')
            print('########################################')
        else:
            print('Свап в Arbswap: нет.')
            print('########################################')

        if self.rpcswap_checked:
            self.checked_projects.append('rpc')
            print('Свап в Rpcswap: да.')
            print(f'Максимальный газ при свапе в Rpcswap (USD): {self.rpcswap_gas_limit}')
            print(f'Максимальный газ при свапе в Rpcswap (ETH): {self.rpcswap_gas_limit_eth}')
            print('########################################')
        else:
            print('Свап в Rpcswap: нет.')
            print('########################################')

        if self.sushiswap_checked:
            self.checked_projects.append('sushi')
            print('Свап в Sushiswap: да.')
            print(f'Максимальный газ при свапе в Sushiswap (USD): {self.sushiswap_gas_limit}')
            print(f'Максимальный газ при свапе в Sushiswap (ETH): {self.sushiswap_gas_limit_eth}')
            print('########################################')
        else:
            print('Свап в Sushiswap: нет.')
            print('########################################')

        print(f'Задержка между проектами в сек. от {self.projects_delay_min} до {self.projects_delay_max}.')
        print(f'Задержка между кошельками в сек. от {self.wallets_delay_min} до {self.wallets_delay_max}.')
        print('########################################')

    def get_private_keys(self):
        with open(self.private_keys_path, 'r') as keys_file:
            keys_list = [row.strip() for row in keys_file]

        return keys_list

    def get_delay_for_wallets(self):
        return random.randint(self.wallets_delay_min, self.wallets_delay_max)

    def get_delay_for_projects(self):
        return random.randint(self.projects_delay_min, self.projects_delay_max)
