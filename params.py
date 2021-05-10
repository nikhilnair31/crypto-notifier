import os
import json

with open('keys.json') as f:
    key_data = json.load(f)

# telegram bot keys
api_key = key_data["telegram_api_key"]
bot_token = key_data["telegram_bot_token"]
chat_id = key_data["telegram_chat_id"]

# twitter api keys
consumer_key = key_data["twitter_consumer_key"]
consumer_secret = key_data["twitter_consumer_secret"]
access_key = key_data["twitter_access_key"]
access_secret = key_data["twitter_access_secret"]

# urls
coin_api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
gecko_api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids=dogecoin'
wazirx_url = 'https://api.wazirx.com/api/v2/tickers'
url_with_token = "https://api.telegram.org/bot{}/".format(bot_token)

# update params
start_loop = False
update_rate = 0.1
time_interval = update_rate * 60

# twitter params
user_name = '@elonmusk'
last_made_tweet = ''
check_coin_in_tweet = ['moon', 'doge', 'DOGE', 'ripple', 'XRP', 'coin', 'crypto', 'currency']

# coin params
coin_name = 'dogeinr'
limit_high = 30
limit_low = 20

# coin params
doge_limits = {"coin_name": "dogeinr", "limit_high" : 30.0, "limit_low" : 20.0, "update_rate" : 0.1}

dir1 = os.path.dirname('root/Projects/crypto-notifier/editable_params.json')
editable_params_filename = os.path.join(dir1, 'editable_params.json')
dir2 = os.path.dirname('root/Projects/crypto-notifier/tracker.py')
tracker_filename = os.path.join(dir2, 'tracker.py')