from bittrex.bittrex import Bittrex
from exchanges.kraken import Kraken
import sys,csv
import time

my_bittrex = Bittrex("-", "-")
result = my_bittrex.get_ticker('BTC-ETH')
Price_ETH_BTC = result.get('result').get('Last')
Price_ETH = Price_ETH_BTC * float(Kraken().get_current_price())
current_datetime = time.strftime("%d/%m/%Y") + " " + time.strftime("%H:%M:%S")

lst=[current_datetime, Price_ETH]

with open("c:\\Users\\robfa\\Desktop\\ETH_Price.csv",'a',newline='') as wr:
    writer = csv.writer(wr, delimiter = ',')
    writer.writerows([lst])
