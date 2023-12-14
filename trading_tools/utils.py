from dotenv import load_dotenv
import os, urllib3, requests

# Load variables from the .env file into the environment
load_dotenv()

API_KEY = os.environ.get("API_KEY")
ACCOUNT_ID = os.environ.get("ACCOUNT_ID")
AUTH_URL = os.environ.get("AUTH_URL")
BTC_WALLET_ID = os.environ.get("BTC_WALLET_ID")
ETH_WALLET_ID = os.environ.get("ETH_WALLET_ID")
USD_WALLET_ID = os.environ.get("USD_WALLET_ID")

BTC_VALUATION_URL = f"https://platform.the-brawl.eu/api/account/{ACCOUNT_ID}/wallet/{BTC_WALLET_ID}/valuation"
ETH_VALUATION_URL = f"https://platform.the-brawl.eu/api/account/{ACCOUNT_ID}/wallet/{ETH_WALLET_ID}/valuation"
TRANSACTION_URL = "http://platform.the-brawl.eu/api/transaction"
COINBASE_BTC_URL = "https://api.coinbase.com/v2/prices/BTC-USD/spot"
COINBASE_ETH_URL = "https://api.coinbase.com/v2/prices/ETH-USD/spot"
COINBASE_TIME_URL = "https://api.coinbase.com/v2/time"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Login data
data = {
    "email": os.environ.get("EMAIL"),  # Insert your email here
    "password": os.environ.get("PASSWORD"),  # Insert your password here
    "returnSecureToken": True,
}

# Authenticate and get the token
auth_res = requests.post(AUTH_URL, json=data, params={"key": API_KEY}).json()
del data

id_token = auth_res["idToken"]
