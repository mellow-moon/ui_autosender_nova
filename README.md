# ui_autosender_nova

Графический интерфейс, позволяющий автоматизировать отправку транзакций в блокчейне Arbitrum Nova.

## Структура проекта

```
- config
  |-abi_config.txt
  |-erc20.json
  |-orbiter_config.py
  |-orbiter_maker.json
  |-swaps_config.py
- data
  |-private_keys.txt
  |-transaction_history.csv
  |-wallets_balances.csv
- img
  |-Arbitrum Nova.png
  |-nova_logo.png
- src
  |-arguments_handler.py
  |-base_router.py
  |-check_balances.py
  |-check_transaction_by_hash.py
  |-create_df_transaction_history.py
  |-make_transactions.py
  |-orbiter.py
  |-utils.py
README.md
main.py
sidebar_interface.ui
sidebar_interface_ui.py
```
