import pandas as pd
from web3 import Web3


with open('config/abi_config.txt', 'r') as conf_file:
    abi_lst = [abi for abi in conf_file]

    abi_token = abi_lst[3]


class BalanceChecker:
    def __init__(self):
        self.usdc_token_address = Web3.to_checksum_address('0x750ba8b76187092B0D1E87E28daaf484d1b5273b')
        self.dai_token_address = Web3.to_checksum_address('0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1')
        self.wbtc_token_address = Web3.to_checksum_address('0x1d05e4e72cd994cdf976181cfb0707345763564d')
        self.weth_token_address = Web3.to_checksum_address('0x722E8BdD2ce80A4422E880164f2079488e115365')
        self.token_addrs = [self.usdc_token_address,
                            self.dai_token_address,
                            self.wbtc_token_address,
                            self.weth_token_address]
        self.abi_token = abi_token
        self.RPC_NOVA = 'https://nova.arbitrum.io/rpc'
        self.RPC_ETH = "https://eth.llamarpc.com"

    def get_balances(self, private_key):
        token_balances = []

        web3 = Web3(Web3.HTTPProvider(self.RPC_NOVA))  # подключение к ноде через HTTP провайдера
        account = web3.eth.account.from_key(private_key)  # получение аккаунта при помощи приватного ключа
        address_wallet = account.address  # получение адреса аккаунта

        for address in self.token_addrs:
            token = web3.eth.contract(address=address, abi=abi_token)
            token_balance = token.functions.balanceOf(address_wallet).call()  # получение баланса токена
            token_balances.append(token_balance)

        return token_balances

    def get_eth_mainnet_balance(self, private_key):
        web3 = Web3(Web3.HTTPProvider(self.RPC_ETH))  # подключение к ноде через HTTP провайдера

        account = web3.eth.account.from_key(private_key)  # получение аккаунта при помощи приватного ключа
        address_wallet = account.address  # получение адреса аккаунта

        # ETH balance
        eth_balance = web3.eth.get_balance(address_wallet)
        eth_balance_decimal = web3.from_wei(eth_balance, 'ether')

        return eth_balance_decimal

    def check_all_balances(self):
        print('Проверка балансов...\n')

        balances_df = pd.DataFrame(columns=['private_key',
                                            'eth_mainnet_balance',
                                            'usdc_balance',
                                            'dai_balance',
                                            'wbtc_balance',
                                            'weth_balance'])

        with open('data/private_keys.txt', 'r') as keys_file:
            keys_list = [row.strip() for row in keys_file]

        for private_key in keys_list:
            eth_balance = self.get_eth_mainnet_balance(private_key)

            token_balances = self.get_balances(private_key)

            balances = [private_key, eth_balance, *token_balances]
            balances_df.loc[len(balances_df)] = balances

        balances_df.to_csv('data/wallets_balances.csv', index=False)

        print('Все балансы были сохранены в файл wallets_balances.csv.')


balance_checker = BalanceChecker()
balance_checker.check_all_balances()
