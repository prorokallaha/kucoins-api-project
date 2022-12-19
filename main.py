from kucoin.client import Client
from time import *
from datetime import datetime
import csv
import json


api_key = '***'
api_secret = '***'
api_passphrase = 'exchangekucoin'

t_date = datetime.now().strftime('%d_%m_%Y')
client = Client(api_key, api_secret, api_passphrase ,sandbox=False)
tickers = client.get_ticker()['ticker']
symbols = []
for symbol in tickers:
    symbols.append(symbol['symbol'])


withraw_history = client.get_withdrawals()
deposit_history = client.get_deposits()


def collect_trades():
    trades = []
    for symbol in symbols:
        transaction_history = client.get_trade_histories(f'{symbol}')
        for info in transaction_history:
            operation = info['side']
            sequence = info['sequence']
            price = info['price']
            size = info['size']
            time = info['time']
            time = datetime.fromtimestamp(time / 1000000000)
            trades.append([time ,symbol, sequence, operation, size, price])
    
    
    with open(f'Trade history - {t_date}.csv', 'a') as file:
        writer = csv.writer(file)
    
        writer.writerow(
            (
                'Date'
                'Name',
                'Sequence',
                'Operation',
                'Size',
                'Price'
            )
        )
    
        writer.writerows(
            trades
        )


# with open('test.json', 'w') as file:
#     withrtaw_items = withraw_history['items']
#     for wi in withrtaw_items:
#         time_info = wi['createdAt']
#         time_info = datetime.fromtimestamp(time_info / 1000)
#         print(time_info)
#     json.dump(withraw_history, file, ensure_ascii=False, indent=4)

def collect_withdrawals():
    result = []
    withrtaw_items = withraw_history['items']
    for wi in withrtaw_items:
        item_currency = wi['currency']
        item_status = wi['status']
        item_adress = wi['address']
        item_amount = wi['amount']
        item_fee = wi['fee']
        item_remark = wi['remark']
        item_time = wi['createdAt']
        item_time = datetime.fromtimestamp(item_time / 1000)
        result.append(
            [item_time, item_currency, item_status, item_amount, item_fee, item_adress, item_remark]
        )

    with open(f'result_withdrawals - {t_date}.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Date',
                'Currency',
                'Status',
                'Amount',
                'Fee',
                'Adress',
                'Remark'
            )
        )

        writer.writerows(
            result
        )


def collect_deposits():
    result = []
    deposit_items = deposit_history['items']
    for di in deposit_items:
        item_currency = di['currency']
        item_status = di['status']
        item_adress = di['address']
        item_amount = di['amount']
        item_time = di['createdAt']
        item_time = datetime.fromtimestamp(item_time / 1000)
        result.append(
            [item_time, item_currency, item_status, item_amount, item_adress]
        )
    with open(f'result_deposits - {t_date}.csv', 'a') as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                'Date',
                'Currency',
                'Status',
                'Amount',
                'Adress'
            )
        )

        writer.writerows(
            result
        )


collect_deposits()
collect_withdrawals()
collect_trades()
