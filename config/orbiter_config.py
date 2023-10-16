import json


with open('config/erc20.json', 'r') as file:
    ERC20_ABI = json.load(file)

with open('config/orbiter_maker.json', 'r') as file:
    ORBITER_MAKER = json.load(file)

ORBITER_AMOUNT = {
    'ethereum': 0.000000000000009001,
    'optimism': 0.000000000000009007,
    'bsc': 0.000000000000009015,
    'arbitrum': 0.000000000000009002,
    'nova': 0.000000000000009016,
    'polygon': 0.000000000000009006,
    'polygon_zkevm': 0.000000000000009017,
    'zksync': 0.000000000000009014,
    'zksync_lite': 0.000000000000009003,
    'starknet': 0.000000000000009004,
}

ORBITER_AMOUNT_STR = {
    'ethereum': '9001',
    'optimism': '9007',
    'bsc': '9015',
    'arbitrum': '9002',
    'nova': '9016',
    'polygon': '9006',
    'polygon_zkevm': '9017',
    'zksync': '9014',
    'zksync_lite': '9003',
    'starknet': '9004',
}

ORBITER_IDS = {
    'ethereum': '1',
    'optimism': '7',
    'bsc': '15',
    'arbitrum': '2',
    'nova': '16',
    'polygon': '6',
    'polygon_zkevm': '17',
    'zksync': '14',
    'zksync_lite': '3',
    'starknet': '4',
}

DATA = {
    'ethereum': {'rpc': 'https://rpc.ankr.com/eth', 'scan': 'https://etherscan.io/tx', 'token': 'ETH'},

    'optimism': {'rpc': 'https://rpc.ankr.com/optimism', 'scan': 'https://optimistic.etherscan.io/tx', 'token': 'ETH'},

    'bsc': {'rpc': 'https://rpc.ankr.com/bsc', 'scan': 'https://bscscan.com/tx', 'token': 'BNB'},

    'polygon': {'rpc': 'https://rpc.ankr.com/polygon', 'scan': 'https://polygonscan.com/tx', 'token': 'MATIC'},

    'polygon_zkevm': {'rpc': 'https://zkevm-rpc.com', 'scan': 'https://zkevm.polygonscan.com/tx', 'token': 'ETH'},

    'arbitrum': {'rpc': 'https://rpc.ankr.com/arbitrum', 'scan': 'https://arbiscan.io/tx', 'token': 'ETH'},

    'avalanche': {'rpc': 'https://rpc.ankr.com/avalanche', 'scan': 'https://snowtrace.io/tx', 'token': 'AVAX'},

    'fantom': {'rpc': 'https://rpc.ankr.com/fantom', 'scan': 'https://ftmscan.com/tx', 'token': 'FTM'},

    'nova': {'rpc': 'https://nova.arbitrum.io/rpc', 'scan': 'https://nova.arbiscan.io/tx', 'token': 'ETH'},

    'zksync': {'rpc': 'https://mainnet.era.zksync.io', 'scan': 'https://explorer.zksync.io/tx', 'token': 'ETH'},
}
