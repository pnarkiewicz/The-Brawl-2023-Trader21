from time import sleep
import pandas as pd
from datetime import datetime
from utils import *
from helper_functions import *
import numpy as np

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
urls = [
    COINBASE_TIME_URL,
    COINBASE_BTC_URL,
    # COINBASE_ETH_URL,
]

BUY = True
SELL = False


class Trader:
    def __init__(self, token, size, alpha, delta, print):
        self.token = token
        self.timestep = 60
        self.opened_positions = []
        self.id_position = 0
        self.all_profit = 0
        self.spread = 0.01

        self.alpha = alpha
        self.delta = delta

        self.total_btc = 0
        self.money = 1000000
        self.max_buy = 1000

        self.btc_prices = []
        self.ema_values = np.array([(1 - self.alpha) ** i for i in range(self.size)])
        self.sum_ema_values = np.sum(self.ema_values)
        self.last_buy = 0
        self.print = print

    # Starts trading loop
    def trade(self, minutes):
        # Get 3 first prices first
        while len(self.btc_prices) < self.size:
            self.update_btc_price()

        while True:
            self.single_trading_loop()

    def single_trading_loop(self):
        self.update_btc_price()
        self.execute_trade()

    def update_btc_price(self):
        new_btc_price = read_btc_price()
        now = datetime.now()
        time_diff = (self.btc_prices[-1][1] - now).total_seconds()

        if len(self.btc_prices) == 0 or (
            new_btc_price > 0 and time_diff > self.timestep
        ):
            self.btc_prices.append([new_btc_price, now])

    def get_decision(self):
        ema = np.sum(self.btc_prices * self.ema_values) / self.sum_ema_values

        if ema > self.delta + self.btc_prices[-1]:
            # print("BUY", ema, self.btc_prices[-1])
            volume = (self.max_buy + self.all_profit / 2) / self.btc_prices[-1]
            return (BUY, volume, self.btc_prices[-1])
        elif ema + self.delta < self.btc_prices[-1] and self.total_btc > 0:
            # print("SELL", ema, self.btc_prices[-1])
            volume = self.total_btc
            return (SELL, volume, 0)
        else:
            return (None, 0, 0)

    def execute_trade(self):
        decision, volume, price = self.get_decision()
        if decision is None:
            pass
        elif decision == BUY:
            buy = buy_btc(volume, price, self.token)
            if buy:
                self.total_btc += volume
                self.last_buy += price * volume
                self.opened_positions.append([volume, price, self.id_position])
                self.id_position += 1
                # print(f"Bought {volume} BTC for {price}")
        elif decision == SELL:
            real_price, sell = sell_btc_none(volume, self.token)
            if sell:
                # print(f"Sold {volume} BTC for {real_price}")
                self.total_btc = 0
                profit = volume * real_price - self.last_buy
                # self.profits.append(
                #     [volume * real_price, self.last_buy, len(self.all_btc_prices) - 1]
                # )
                if self.print:
                    print(
                        f"Profit: {profit:.3f} USD. Percentage profit: {100*profit/self.last_buy:.3f}%"
                    )
                self.all_profit += profit
                if self.print:
                    print(f"Overall profit: {self.all_profit:.3f} USD")
                self.last_buy = 0

    def get_current_stats(self):
        return {
            # "Profits": self.profits,
            # "All_profits": self.all_profit,
            # "BTC_price": self.all_btc_prices,
        }


# trader = Trader(id_token, 15, 0.3, 3, True)
# stats = trader.trade(1e4)
