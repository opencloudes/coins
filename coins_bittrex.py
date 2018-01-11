from bittrex.bittrex import *
import os
import sys
import time
import json

def bittrex_exchange( tckr ):
    #my_bittrex = Bittrex(None, None, api_version=API_V2_0)  # or defaulting to v1.1 as Bittrex(None, None)
    my_bittrex = Bittrex(None, None)
    markets=my_bittrex.get_markets()
    eth=my_bittrex.get_currencies()
    ltc=my_bittrex.get_ticker('BTC-LTC')
    if tckr :
        ticker = my_bittrex.get_ticker(tckr)
        ticker_json = json.dumps(ticker)
        parsed_json = json.loads(ticker_json)
        results = parsed_json['result']
        results_json = json.dumps(results)
        result_json = json.loads(results_json)
        return result_json

changes = ['BTC-UBQ', 'BTC-XMY', 'BTC-DOGE', 'BTC-RDD', 'BTC-ABY', 'BTC-BTC', 'BTC-ETH', 'BTC-LTC']
x = 1
for i in range(len(changes)):
    x = x+1
    if changes[i] != 'BTC-BTC':
        btc_change = bittrex_exchange(changes[i])
    else:
        btc_change_json = json.dumps({"Ask": 1,"Bid": 1,"Last": 1})
        btc_change = json.loads(btc_change_json)
    range_ = 'Coins!K'+str(x)+':K'+str(x)
    print(changes[i])
    print(btc_change)
    print(range_)
