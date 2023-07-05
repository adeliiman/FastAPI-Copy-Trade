from binance.um_futures import UMFutures


def new_position(api_key, secret_key, leverage, percent, signal):
    print('new position ........')
    proxies = { 'https': 'http://127.0.0.1:44129' }
    client = UMFutures(key=api_key, secret=secret_key, base_url="https://testnet.binancefuture.com", proxies=proxies)


    def get_balance():
        assets = client.balance()
        for asset in assets:
            if asset['asset'] == 'USDT':
                balance = float(asset["availableBalance"])
                return balance

    try:
        balance = get_balance()
        size = round( (balance*percent) / float(signal['price']), 3)
        client.change_leverage(symbol=signal['symbol'], leverage=leverage)

        side = "BUY" if signal['side'] == "Long" else "SELL"
        # Post a new order
        params = {
            'symbol': signal['symbol'],
            'side': side, # SELL/BUY
            'type': 'MARKET',
            'quantity': size,
        }

        response = client.new_order(**params)
        print(response)
        return response['orderId']
    except Exception as e:
        print(e)











# api_key = "bd74082ca7357a058346e12cec5e3fdf045c95b3b36fbe3188046186d6e7dad7"
# api_secret = "6b3fc8deddfad611d11fba622c4516f3831a1d5af50d60bd48d3362fc576ef8f"
# proxies = { 'https': 'http://127.0.0.1:44129' }

# client = UMFutures(api_key, api_secret, base_url="https://testnet.binancefuture.com", proxies=proxies)



# try:
#     def get_balance():
#         assets = client.balance()
#         for asset in assets:
#             if asset['asset'] == 'USDT':
#                 balance = float(asset["availableBalance"])
#                 print(f'balance = {balance} -------')
#                 return balance
#     balance = get_balance()
#     percent = 10/100
#     leverage=10
#     price = 30600
#     size = (balance*percent) / float(price)
#     size = round(size, 3)
#     print(f"size= {size}   --------value($) = {balance*percent}")

#     params = {
#     'symbol': 'BTCUSDT',
#     'side': 'SELL', # SELL/BUY
#     'type': 'MARKET',
#     'quantity': size,
#     }

#     print(client.change_leverage(symbol="BTCUSDT", leverage=leverage))
#     print('................................')

#     response = client.new_order(**params)
#     print(response)
#     print('................................')

#     response = client.get_position_risk(symbol='BTCUSDT')
#     print(response)
#     print('................................')

#     response = client.get_account_trades(symbol='BTCUSDT')
#     print(response[-1])
#     print('................................')

#     balance = get_balance()
# except Exception as e:
#     print(e)