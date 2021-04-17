import params

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
    url = 'https://api.telegram.org/bot'+params.bot_token+'/sendMessage?chat_id='+params.chat_id+'&text='+msg
    requests.get(url)

# Function to extract tweets
def get_tweets(username):
    global api
    for status in tweepy.Cursor(api.user_timeline, screen_name=username, count=None, since_id=None, max_id=None, trim_user=True, exclude_replies=True, contributor_details=False, include_entities=False).items(1):
        print('most recent status.text;\n', status.text+"\n")
        if(params.last_made_tweet != status.text):
            params.last_made_tweet = status.text
            if any(x in params.last_made_tweet.lower() for x in params.check_coin_in_tweet):
                print("Has doge in params.last_made_tweet\n")
                send_message(msg = username+ 'Tweet :\n' +params.last_made_tweet)

# make a request to the wazirx api
def wx_get_btc_price(doge_looky):
    url = params.wazirx_url
    response = requests.get(url)
    response_json = response.json()
    doge_price = response_json[doge_looky]
    print('wx_get_btc_price doge_price[last]: ', doge_price['last'])
    return float(doge_price['last'])

# compare prices with limits
def pricer():
    doge_price = wx_get_btc_price(params.doge_looky)
    print('doge_price: ', doge_price)
    print('params.doge_low: ', params.doge_low)
    print('params.doge_high: ', params.doge_high)

    if doge_price > params.doge_high:
        send_message(msg='DOGE Price Spike Alert: '+ str(doge_price))
    if doge_price < params.doge_low:
        send_message(msg='DOGE Price Drop Alert: '+ str(doge_price))
    
    get_tweets(params.user_name)

def main():
    init_twitter()
    while True:
        pricer()
        time.sleep(params.time_interval)

if __name__ == '__main__':
    main()