import os

# telegram bot keys
api_key = 'd3a0e65f-a376-4512-80c1-1472391a929c'
bot_token = '1697782782:AAH5FsAWh7UBSMZcr0O7iYI2yX35cnJVus8'
chat_id = '803618321'

# urls
coin_api_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
gecko_api_url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=inr&ids=dogecoin'
wazirx_url = 'https://api.wazirx.com/api/v2/tickers'
url_with_token = "https://api.telegram.org/bot{}/".format(bot_token)

# twitter api keys
consumer_key = "qboeodsSEEVY8mz8b8t5fsu9y" 
consumer_secret = "hu7acIT64TEejNf9bPvysB9mwadjssqmD8ny3eE1jcuyyFxsy9"
access_key = "2441129845-KIw0UFenFwpZToRAWUHqUGPXFhc2jd6KKNMNyCz"
access_secret = "qGs6FHGLQ071zm6vcM8muF1PI9eO0jFIelHQC8HL6oHI5"

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

dir = os.path.dirname('root/Projects/crypto-notifier/editable_params.json')
filename = os.path.join(dir, 'editable_params.json')
