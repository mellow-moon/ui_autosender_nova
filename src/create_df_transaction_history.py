import csv

with open('transaction_history.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ['private_key',
             'Хеш транзакции',
             'Время транзакции',
             'Тип транзакции',
             'Продажа',
             'Покупка',
             'Объем транзакции', 'Комиссия']
    
    writer.writerow(field)
