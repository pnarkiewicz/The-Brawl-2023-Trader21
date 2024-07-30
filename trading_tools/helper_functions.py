import requests
from concurrent.futures import ThreadPoolExecutor
import json
from utils import COINBASE_TIME_URL, COINBASE_ETH_URL, COINBASE_BTC_URL
from datetime import datetime
from utils import *

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
session_coinbase = requests.Session()
session_contest = requests.Session()


def make_request(url):
    response = session_coinbase.get(url)
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
        "BTC_price": float(data[COINBASE_BTC_URL]["data"]["amount"]),
        "ETH_price": float(data[COINBASE_ETH_URL]["data"]["amount"]),
    }


# returns True if purchase is completed
def buy_btc(volume, price, token):
    # print(f"Buying {volume} BTC for {price} per unit USD, total: {volume * price} USD")
    try:
        res = session_contest.post(
            TRANSACTION_URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "sourceWalletId": USD_WALLET_ID,
                "destWalletId": BTC_WALLET_ID,
                "amountFromSourceWallet": price * volume,
                "exchangeRate": 1 / price,
            },
            verify=False,
        ).json()

        return "data" in res.keys()
    except:
        print("BUY BTC ERROR")
        return False


# returns True if sale is completed
def sell_btc(volume, price, token):
    # print(f"Selling {volume} BTC for {price} USD, total: {volume * price} USD")
    try:
        res = session_contest.post(
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
    except:
        print("SELL BTC ERROR")
        return False


def sell_btc_none(volume, token):
    try:
        res = session_contest.post(
            TRANSACTION_URL,
            headers={"Authorization": f"Bearer {token}"},
            json={
                "sourceWalletId": BTC_WALLET_ID,
                "destWalletId": USD_WALLET_ID,
                "amountFromSourceWallet": volume,
            },
            verify=False,
        ).json()

        if "data" not in res.keys():
            return 0, False
        else:
            real_price = float(res["data"][0]["attributes"]["exchangeRate"])
            return real_price, "data" in res.keys()
    except:
        print("SELL BTC NONE ERROR")
        return 0, False


def read_btc_price():
    try:
        response = session_contest.get(url, headers=headers, verify=False)
        if response.status_code == 200:
            return float(response.json()["rates"]["ticker"]["lastTrade"]["p"])
        else:
            return -1
    except:
        print("READ BTC PRICE ERROR")
        return -1
