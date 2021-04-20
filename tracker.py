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
def wx_get_btc_price(coin_name):
    url = params.wazirx_url
    response = requests.get(url)
    if('json' in response.headers.get('Content-Type')):
        response_json = response.json()
        coin_price = response_json[coin_name]
        return float(coin_price['last'])
    else:
        return None

# compare prices with limits
def pricer():
    with open(params.editable_params_filename) as jsonFile:
        data = json.load(jsonFile)
        coin_price = wx_get_btc_price(data["coin_name"])
        print(f'data["coin_name"]: {data["coin_name"]}')
        print(f'data["limit_low"]: {data["limit_low"]}')
        print(f'data["limit_high"]: {data["limit_high"]}')
        print(f'coin_price: {coin_price}')

        if coin_price == None:
            print(f'Something messed up at requests.get(url).json()')
        else:
            if coin_price > data["limit_high"]:
                send_message(msg=f'Price Spike Alert: {coin_price}')
            if coin_price < data["limit_low"]:
                send_message(msg=f'Price Drop Alert: {coin_price}')
        
        get_tweets(params.user_name)

def main():
    init_twitter()
    while True:
        pricer()
        time.sleep(params.doge_limits["update_rate"])

if __name__ == '__main__':
    main()