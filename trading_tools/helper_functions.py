import requests
from concurrent.futures import ThreadPoolExecutor
import json
from utils import COINBASE_TIME_URL, COINBASE_ETH_URL, COINBASE_BTC_URL
from datetime import datetime
from utils import *

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"


def make_request(url):
    response = requests.get(url)
    return response.text


def make_multiple_requests(urls, max_workers=3):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        responses = list(executor.map(make_request, urls))

    data = {}
    for url, response in zip(urls, responses):
        data[url] = json.loads(response)

    return data


# data is returned from make_multiple_requests
def read_off_crypto_data(data):
    return {
        "Epoch": int(data[COINBASE_TIME_URL]["data"]["epoch"]),
        "Time": datetime.strptime(
            data[COINBASE_TIME_URL]["data"]["iso"], DATETIME_FORMAT
        ),
        "BTC_price": float(data[COINBASE_BTC_URL]["data"]["amount"]),
        "ETH_price": float(data[COINBASE_ETH_URL]["data"]["amount"]),
    }


def buy_btc(volume, price, token):
    # print(f"Buying {volume} BTC for {price} per unit USD, total: {volume * price} USD")
    res = requests.post(
        TRANSACTION_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "sourceWalletId": USD_WALLET_ID,
            "destWalletId": BTC_WALLET_ID,
            "amountFromSourceWallet": price * volume,
            "exchangeRate": 1 / price,
        },
        verify=False,
    )
    return "data" in res.json().keys()


def sell_btc(volume, price, token):
    # print(f"Selling {volume} BTC for {price} USD, total: {volume * price} USD")
    res = requests.post(
        TRANSACTION_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "sourceWalletId": BTC_WALLET_ID,
            "destWalletId": USD_WALLET_ID,
            "amountFromSourceWallet": volume,
            "exchangeRate": price,
        },
        verify=False,
    )
    return "data" in res.json().keys()


def sell_btc_none(volume, token):
    res = requests.post(
        TRANSACTION_URL,
        headers={"Authorization": f"Bearer {token}"},
        json={
            "sourceWalletId": BTC_WALLET_ID,
            "destWalletId": USD_WALLET_ID,
            "amountFromSourceWallet": volume,
        },
        verify=False,
    )
    return "data" in res.json().keys()
