from params import *
from init import *

import sys
import tweepy
import requests
import time
import json

# message from bot to user
def send_message(chat_id, msg):
    url = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+chat_id+'&text='+msg
    requests.get(url)

# Function to extract tweets
def get_tweets(username):
    global last_made_tweet, check_coin_in_tweet
    for status in tweepy.Cursor(api.user_timeline, screen_name=username, count=None, since_id=None, max_id=None, trim_user=True, exclude_replies=True, contributor_details=False, include_entities=False).items(number_of_tweets):
        print('most recent status.text;\n', status.text+"\n")
        if(last_made_tweet != status.text):
            last_made_tweet = status.text
            if any(x in last_made_tweet.lower() for x in check_coin_in_tweet):
                print("Has doge in last_made_tweet\n")
                send_message(chat_id=chat_id, msg= username+ 'Tweet :\n' +last_made_tweet)

# make a request to the wazirx api
def wx_get_btc_price(doge_looky):
    url = wazirx_url
    response = requests.get(url)
    response_json = response.json()
    doge_price = response_json[doge_looky]
    print('wx_get_btc_price doge_price[last]: ', doge_price['last'])
    return float(doge_price['last'])

# compare prices with limits
def pricer():
    doge_price = wx_get_btc_price(doge_looky)
    print('doge_price: ', doge_price)
    print('doge_low: ', doge_low)
    print('doge_high: ', doge_high)

    if doge_price > doge_high:
        send_message(chat_id=chat_id, msg='DOGE Price Spike Alert: '+ str(doge_price))
    if doge_price < doge_low:
        send_message(chat_id=chat_id, msg='DOGE Price Drop Alert: '+ str(doge_price))
    
    get_tweets(user_name)

def main():
    global updater
    last_textchat = None

    while True:
        pricer()
        time.sleep(time_interval)

if __name__ == '__main__':
    main()