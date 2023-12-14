from time import sleep
import pandas as pd
from datetime import datetime
from utils import *
from helper_functions import *

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


class Trader:
    def __init__(self, token, strategy):
        self.token = token
        self.strategy = strategy
        self.wait = (True, 2)
        self.size = 8
        self.data = pd.DataFrame(
            {"Time": [], "Epoch": [], "BTC_price": [], "ETH_price": []}
        )
        self.data["Time"] = pd.to_datetime(self.data["Time"], format=DATETIME_FORMAT)
        self.data["BTC_price"] = self.data["BTC_price"].astype(float)
        self.data["ETH_price"] = self.data["ETH_price"].astype(float)
        self.data["Epoch"] = self.data["Epoch"].astype(int)
        self.epochs = 0
        self.eps = 4

    # Starts trading loop
    def trade(self):
        # Get 3 first prices first
        while len(self.data) < 3:
            self.update_prices()

        while True:
            self.single_trading_loop()

    def single_trading_loop(self):
        self.update_prices()
        self.execute_trade()

    def update_prices(self):
        urls = [
            COINBASE_TIME_URL,
            COINBASE_BTC_URL,
            COINBASE_ETH_URL,
        ]
        new_data = read_off_crypto_data(make_multiple_requests(urls))

        if (
            len(self.data) == 0
            or new_data["Epoch"] != self.data.iloc[len(self.data) - 1]["Epoch"]
        ):
            self.data.loc[self.epochs] = new_data
            self.epochs += 1
            if len(self.data) > self.size:
                self.data = self.data.iloc[1:]

    def execute_trade(self):
        row_current = self.data.loc[self.epochs - 1]
        row_previous = self.data.loc[self.epochs - 2]

        eth_prices = (row_previous["ETH_price"], row_current["ETH_price"])
        btc_prices = (row_previous["BTC_price"], row_current["BTC_price"])

        volume = 0.0001

        if btc_prices[0] + 10 < btc_prices[1]:
            buy = buy_btc(volume, btc_prices[0] + self.eps, self.token)
            print(f"Last btc prices: {btc_prices}")
            print(f"{volume} bitcoin was bought: {buy} for {btc_prices[0] + self.eps}")
            if buy:
                k = 0
                sell = False
                while k < 50 and not sell:
                    sell = sell_btc(volume, btc_prices[1] - self.eps, self.token)
                    sleep(0.001)

                if sell:
                    print(
                        f"{volume} bitcoin was sold: {sell} at {btc_prices[1] - self.eps}"
                    )

                k = 0
                sold = False
                while k < 50 and not sold:
                    sold = sell_btc_none(volume, self.token)

                if sold:
                    print(f"{volume} bitcoin was sold potentailly without profit.")
