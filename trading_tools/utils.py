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

# URL of the API
url = "https://platform.the-brawl.eu/ui/api/rates?currencyId=BTC&type=current"

# Headers
headers = {
    "authority": "platform.the-brawl.eu",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8,pl;q=0.7",
    "cache-control": "max-age=0",
    "cookie": "_ga=GA1.1.1273563410.1702031817; connect.sid=s%3Aj7CTFkw3WubU7VoMUphEKdZccBXhqljY.onbbx7GdAKHqWRowPJWavbLkL%2Fp4eQlJoF1Cd9p%2B3kw; cryptobrawl.AuthUser=IntcImlkXCI6XCJHbGpiakE4a1dqV2lHS2FrUEV2S3VlQjZHODEyXCIsXCJjbGFpbXNcIjp7fSxcImVtYWlsXCI6XCJwbjQ1ODg2NkBzdHVkZW50cy5taW11dy5lZHUucGxcIixcImVtYWlsVmVyaWZpZWRcIjp0cnVlLFwiZGlzcGxheU5hbWVcIjpcIlBhd2VsXCIsXCJjbGllbnRJbml0aWFsaXplZFwiOmZhbHNlfSI=; cryptobrawl.AuthUser.sig=prGKP_opFy9YWZZc3i0bTgTwE_Y; _ga_85WP5H5EX2=GS1.1.1702626284.38.0.1702626284.0.0.0; cryptobrawl.AuthUserTokens=IntcImlkVG9rZW5cIjpcImV5SmhiR2NpT2lKU1V6STFOaUlzSW10cFpDSTZJbUpsTnpneU0yVm1NREZpWkRSa01tSTVOakkzTkRFMk5UaGtNakE0TURkbFptVmxObVJsTldNaUxDSjBlWEFpT2lKS1YxUWlmUS5leUp1WVcxbElqb2lVR0YzWld3aUxDSnBjM01pT2lKb2RIUndjem92TDNObFkzVnlaWFJ2YTJWdUxtZHZiMmRzWlM1amIyMHZZM0o1Y0hSdk1qTXROV0ZsTVRFaUxDSmhkV1FpT2lKamNubHdkRzh5TXkwMVlXVXhNU0lzSW1GMWRHaGZkR2x0WlNJNk1UY3dNall5TmpJNE5Dd2lkWE5sY2w5cFpDSTZJa2RzYW1KcVFUaHJWMnBYYVVkTFlXdFFSWFpMZFdWQ05rYzRNVElpTENKemRXSWlPaUpIYkdwaWFrRTRhMWRxVjJsSFMyRnJVRVYyUzNWbFFqWkhPREV5SWl3aWFXRjBJam94TnpBeU5qSTJNamcwTENKbGVIQWlPakUzTURJMk1qazRPRFFzSW1WdFlXbHNJam9pY0c0ME5UZzROalpBYzNSMVpHVnVkSE11YldsdGRYY3VaV1IxTG5Cc0lpd2laVzFoYVd4ZmRtVnlhV1pwWldRaU9uUnlkV1VzSW1acGNtVmlZWE5sSWpwN0ltbGtaVzUwYVhScFpYTWlPbnNpWlcxaGFXd2lPbHNpY0c0ME5UZzROalpBYzNSMVpHVnVkSE11YldsdGRYY3VaV1IxTG5Cc0lsMTlMQ0p6YVdkdVgybHVYM0J5YjNacFpHVnlJam9pWTNWemRHOXRJbjE5LlExRjdTOUdjTDBPWFZXWl9HSUdWNy0xc1lGMUZuQ0REMGhqVkY3VTVkYzRkc1Z0NTFlanhfNW04bDRpdnBtQ0NiT2NfcV9LcGFXTXg5MzkwMUoyMGpfN0tpVmNSZjNTeVdlMGo1S3pGSmVfOWxuM2MzclBockRlZ0VTNHV4blVDU3NzM1NSQUtkSlo0MVdRQTlXY0NKWThVWGF2ak1BQnNxdUJLUVpSdDdQYU5HdkwxSVdueldmUjhHUG1YTkpBeTc5RGIyamUzTUJhVGplWXFBZzgxQTdCMjk5bWpFczAyOG9DTVo4UFhLeXNVWWFsYmtFUFdNenJlS1FsSVJEaElCdUtzVEU4eC1jVTVPdjBoUGpoR1puMFh6ZTFySkEwYW1WSW1BNEs5N2w4bm1wVkdHT2hnYXJIaTBlOTNrVm50TjZSdGw5N0g0V2hQY2FwaGtmTlY0QVwiLFwicmVmcmVzaFRva2VuXCI6XCJBTWYtdkJ5ZWZSUEdRbHRsb3RRRkZLdmQyWThUWTdzamxOZGNLUXY1TEFZblRTWGdnbU1zT25MSHNEbUdiLTBwNG9ReTFBdm9EUkVwOFMwenJ1d0NoQ2NVRUpacEFJYWpCd0ROSzRXOVhoakhrRndPOG5RNTlzWWNVYnBOVng1eWFreDNYQXNaWEtueWRHMHM0U0FhVGRMaE4zZlloa0FqTVBsOGxla3ZVUW1VR2tUT3o1V2ZwS29cIn0i; cryptobrawl.AuthUserTokens.sig=BkbFhSCLCg5m-ULHlqyCxECWrLo",
    "if-none-match": '"24a-KVY3R5JRe8if66f102/e+gBdqRI"',
    "sec-ch-ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
}
