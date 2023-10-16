import sys
import time
import random

from arguments_handler import ArgumentsHandler
from base_router import BaseRouter
from orbiter import Orbiter

handler = ArgumentsHandler(*sys.argv[1:])
router = BaseRouter()
orbiter_bridger = Orbiter()

keys_list = handler.get_private_keys()

print('Скрипт начал работу.')

for private_key in keys_list:
    time.sleep(handler.get_delay_for_wallets())

    if handler.orbiter_bridge_checked:
        print('Бридж в Orbiter Finance.')
        orbiter_bridger.orbiter_bridge(private_key,
                                       handler.orbiter_bridge_limit_min_eth,
                                       handler.orbiter_bridge_limit_max_eth,
                                       handler.orbiter_bridge_gas_limit.eth)

        time.sleep(handler.get_delay_for_projects())
    
    for _ in range(handler.transaction_count):
        # если checked_projects не пуст
        if not handler.checked_projects == []:
            swap_router = None
            abi = None
            amount = None

            exchange = random.choice(handler.checked_projects)

            token = random.choice(router.token_arr)

            match exchange:
                case 'rpc':
                    router.swap(private_key,
                                router.rpc_router,
                                router.abi_rpc,
                                round(random.uniform(handler.rpcswap_limit_min_eth,
                                                     handler.rpcswap_limit_max_eth),
                                      8),
                                token['address'],
                                token['symbol'],
                                handler.rpcswap_gas_limit_eth)
                case 'sushi':
                    router.swap(private_key,
                                router.sushi_router,
                                router.abi_sushi,
                                round(random.uniform(handler.sushiswap_limit_min_eth,
                                                     handler.sushiswap_limit_max_eth),
                                      8),
                                token['address'],
                                token['symbol'],
                                handler.sushiswap_gas_limit_eth)
                case 'arb':
                    router.swap(private_key,
                                router.arb_router,
                                router.abi_arb,
                                round(random.uniform(handler.arbswap_limit_min_eth,
                                                     handler.arbswap_limit_max_eth),
                                      8),
                                token['address'],
                                token['symbol'],
                                handler.arbswap_gas_limit_eth)

print('Все транзакции были проведены.')
