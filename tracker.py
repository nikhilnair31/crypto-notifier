import params

import os
import sys
import tweepy
import requests
import time
import json

# initialize twitter api
def init_twitter():
    global api
    auth = tweepy.OAuthHandler(params.consumer_key, params.consumer_secret)
    auth.set_access_token(params.access_key, params.access_secret)
    api = tweepy.API(auth)

# message from bot to user
def send_message(msg):
    url = f'https://api.telegram.org/bot{params.bot_token}/sendMessage?chat_id={params.chat_id}&text={msg}'
    requests.get(url)

# Function to extract tweets
def get_tweets(username):
    global api
    for status in tweepy.Cursor(api.user_timeline, screen_name=username, count=None, since_id=None, max_id=None, trim_user=True, exclude_replies=True, contributor_details=False, include_entities=False).items(1):
        print(f'most recent status.text;\n{status.text}\n')
        if(params.last_made_tweet != status.text):
            params.last_made_tweet = status.text
            if any(x in params.last_made_tweet.lower() for x in params.check_coin_in_tweet):
                print(f'Has doge in params.last_made_tweet\n')
                send_message(msg = f'{username} Tweet :\n{params.last_made_tweet}')

# make a request to the wazirx api
def wx_get_btc_price(coin_looky):
    url = params.wazirx_url
    response = requests.get(url)
    if('json' in response.headers.get('Content-Type')):
        response_json = response.json()
        print(f'response_json: {response_json}\n')
        doge_price = response_json[coin_looky]
        print(f'wx_get_btc_price doge_price[last]: {doge_price["last"]}')
        return float(doge_price['last'])
    else:
        return 0.0

# compare prices with limits
def pricer():
    doge_price = wx_get_btc_price(params.coin_looky)
    fileDir = os.path.dirname(os.path.realpath('/home/pi/Projects/crypto-notifier/editable_params.json'))
    filename = os.path.join(fileDir, 'editable_params.json')
    with open(filename) as jsonFile:
        data = json.load(jsonFile)
        print(f'doge_price: {doge_price}')
        print(f'data["limit_low"]: {data["limit_low"]}')
        print(f'data["limit_high"]: {data["limit_high"]}')

        if doge_price > data["limit_high"]:
            send_message(msg=f'DOGE Price Spike Alert: {str(doge_price)}')
        if doge_price < data["limit_low"]:
            send_message(msg=f'DOGE Price Drop Alert: {str(doge_price)}')
        
        get_tweets(params.user_name)

def main():
    init_twitter()
    while True:
        pricer()
        time.sleep(params.time_interval)

if __name__ == '__main__':
    main()
