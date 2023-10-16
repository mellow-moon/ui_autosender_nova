import sys
import csv
import os

import pandas

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QHeaderView, QTableWidgetItem

from sidebar_interface_ui import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # боковое меню
        self.ui.menu_transaction.clicked.connect(lambda: self.ui.stacked_widget.setCurrentIndex(0))
        self.ui.menu_accounts.clicked.connect(lambda: self.ui.stacked_widget.setCurrentIndex(1))
        self.ui.menu_check_hash.clicked.connect(lambda: self.ui.stacked_widget.setCurrentIndex(2))
        self.ui.menu_transaction_history.clicked.connect(lambda: self.ui.stacked_widget.setCurrentIndex(3))

        self.ui.menu_transaction.clicked.connect(lambda: self.change_page(self.ui.menu_transaction))
        self.ui.menu_accounts.clicked.connect(lambda: self.change_page(self.ui.menu_accounts))
        self.ui.menu_check_hash.clicked.connect(lambda: self.change_page(self.ui.menu_check_hash))
        self.ui.menu_transaction_history.clicked.connect(lambda: self.change_page(self.ui.menu_transaction_history))

        # сигналы на кнопки
        self.ui.start_btn.clicked.connect(self.make_transactions)
        self.ui.show_transactions_history_btn.clicked.connect(self.return_transaction_history)
        self.ui.accounts_btn_check_balances.clicked.connect(self.balances_check_if_button_clicked)
        self.ui.check_hash_btn.clicked.connect(self.check_transaction_status)

        # таблица с балансами аккаунтов
        self.ui.balances_table.setHorizontalHeaderLabels(['private_key',
                                                          'ETH',
                                                          'USDC',
                                                          'DAI',
                                                          'WBTC',
                                                          'WETH'])
        self.ui.balances_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.balances_table.horizontalHeader().setVisible(True)

        # таблица с транзакциями
        self.ui.transaction_history_table.setHorizontalHeaderLabels(['private_key',
                                                                     'Хеш',
                                                                     'Время',
                                                                     'Тип',
                                                                     'Продажа',
                                                                     'Покупка',
                                                                     'Объем'])
        self.ui.transaction_history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ui.transaction_history_table.horizontalHeader().setVisible(True)

        # проверки
        self.orbiter_bridge_checked = self.ui.checker_orbiter_bridge.checkState()
        self.abrswap_checked = self.ui.checker_arbswap.checkState()
        self.rpcswap_checked = self.ui.checker_rpcswap.checkState()
        self.sushiswap_checked = self.ui.checker_sushiswap.checkState()

        # выставление лимитов
        self.orbiter_bridge_limit_min = self.ui.orbiter_bridge_limit_min.text()
        self.orbiter_bridge_limit_max = self.ui.orbiter_bridge_limit_max.text()

        self.arbswap_limit_min = self.ui.arbswap_limit_min.text()
        self.arbswap_limit_max = self.ui.arbswap_limit_max.text()

        self.rpcswap_limit_min = self.ui.rpcswap_limit_min.text()
        self.rpcswap_limit_max = self.ui.rpcswap_limit_max.text()

        self.sushiswap_limit_min = self.ui.sushiswap_limit_min.text()
        self.sushiswap_limit_max = self.ui.sushiswap_limit_max.text()

        # выставление лимитов газа
        self.orbiter_bridge_gas_limit = self.ui.max_gas_fee_orbiter.text()
        self.arbswap_gas_limit = self.ui.max_gas_fee_arbswap.text()
        self.rpcswap_gas_limit = self.ui.max_gas_fee_rpcswap.text()
        self.sushiswap_gas_limit = self.ui.max_gas_fee_sushiswap.text()

        # задержки между проектами
        self.projects_delay_min = self.ui.projects_delay_min.text()
        self.projects_delay_max = self.ui.projects_delay_max.text()

        # задержки между кошельками
        self.wallets_delay_min = self.ui.wallets_delay_min.text()
        self.wallets_delay_max = self.ui.wallets_delay_max.text()

        # подсчет числа транзакций
        self.transactions_count = self.ui.transactions_count_input.text()

        # кнопки
        self.btn_list = self.ui.frame_2.findChildren(QPushButton)

        self.resize(1200, 800)
    
    def make_transactions(self):
        arguments = [self.orbiter_bridge_checked,
                     self.abrswap_checked,
                     self.rpcswap_checked,
                     self.sushiswap_checked,
                     self.orbiter_bridge_limit_min,
                     self.orbiter_bridge_limit_max,
                     self.arbswap_limit_min,
                     self.arbswap_limit_max,
                     self.rpcswap_limit_min,
                     self.rpcswap_limit_max,
                     self.sushiswap_limit_min,
                     self.sushiswap_limit_max,
                     self.projects_delay_min,
                     self.projects_delay_max,
                     self.wallets_delay_min,
                     self.wallets_delay_max,
                     self.transactions_count,
                     self.orbiter_bridge_gas_limit,
                     self.arbswap_gas_limit,
                     self.rpcswap_gas_limit,
                     self.sushiswap_gas_limit
                     ]

        # запуск скрипта в cmd
        os.system(rf'start cmd /k python src/make_transactions.py {" ".join(str(arg) for arg in arguments)}')

    def change_page(self, target_btn):
        for btn in self.btn_list:
            btn.setStyleSheet('background-color: transparent')
        
        target_btn.setStyleSheet('background-color: #1f232a;')
    
    def return_transaction_history(self):
        df_transactions = pandas.read_csv('data/transaction_history.csv')

        if not df_transactions.empty:
            reversed_df = df_transactions.iloc[::-1]
            df_rows_count = reversed_df.shape[0]

            if df_rows_count > 100:
                reversed_df = reversed_df.iloc[:100]

            self.ui.transaction_history_table.setRowCount(0)

            for _, tx_row in reversed_df.iterrows():
                row_position = self.ui.transaction_history_table.rowCount()
                self.ui.transaction_history_table.insertRow(row_position)
                self.ui.transaction_history_table.setItem(row_position, 0, QTableWidgetItem(str(tx_row[0])))
                self.ui.transaction_history_table.setItem(row_position, 1, QTableWidgetItem(str(tx_row[1])))
                self.ui.transaction_history_table.setItem(row_position, 2, QTableWidgetItem(str(tx_row[2])))
                self.ui.transaction_history_table.setItem(row_position, 3, QTableWidgetItem(str(tx_row[3])))
                self.ui.transaction_history_table.setItem(row_position, 4, QTableWidgetItem(str(tx_row[4])))
                self.ui.transaction_history_table.setItem(row_position, 5, QTableWidgetItem(str(tx_row[5])))
                self.ui.transaction_history_table.setItem(row_position, 6, QTableWidgetItem(str(tx_row[6])))

        else:
            os.system(rf'start cmd /k echo Не было совершено ни одной транзакции, история пуста!')
    
    def balances_check_if_button_clicked(self):
        os.system(r'start cmd /k python src/check_balances.py')
        
        self.ui.balances_table.setRowCount(0)
        
        with open('data/wallets_balances.csv', 'r') as balances_file:
            balance_reader = csv.reader(balances_file, delimiter=' ', quotechar='|')
            next(balance_reader, None)
            for row in balance_reader:
                balances_list = row[0].split(',')
                
                private_key = balances_list[0]
                eth_balance = balances_list[1]
                usdc_balance = balances_list[2]
                dai_balance = balances_list[3]
                wbtc_balance = balances_list[4]
                weth_balance = balances_list[5]

                row_position = self.ui.balances_table.rowCount()
                self.ui.balances_table.insertRow(row_position)
                self.ui.balances_table.setItem(row_position, 0, QTableWidgetItem(private_key))
                self.ui.balances_table.setItem(row_position, 1, QTableWidgetItem(str(eth_balance)))
                self.ui.balances_table.setItem(row_position, 2, QTableWidgetItem(str(usdc_balance)))
                self.ui.balances_table.setItem(row_position, 3, QTableWidgetItem(str(dai_balance)))
                self.ui.balances_table.setItem(row_position, 4, QTableWidgetItem(str(wbtc_balance)))
                self.ui.balances_table.setItem(row_position, 5, QTableWidgetItem(str(weth_balance)))

    def check_transaction_status(self):
        tx_hash = self.ui.check_hash_input.text()
        
        os.system(rf'start cmd /k python src/check_transaction_by_hash.py {tx_hash}')


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
