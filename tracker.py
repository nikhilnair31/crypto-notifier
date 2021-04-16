from params import *
import tweepy
import requests
import time
import json

# Function to extract tweets
def get_tweets(username):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    number_of_tweets = 5
    for status in tweepy.Cursor(api.user_timeline, screen_name=username, count=None, since_id=None, max_id=None, trim_user=True, exclude_replies=True, contributor_details=False, include_entities=False).items(number_of_tweets):
        print(status.text+"\n<------------------------------->\n")

def get_updates():
    url = url_with_token + "getUpdates"
    response = requests.get(url)
    content = response.content.decode("utf8")
    js = json.loads(content)
    return js

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return text

# make a request to the coinmarketcap api
def cm_get_btc_price():
    url = coin_api_url
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key
    }
    parameters = {
        'start':'1',
        'limit':'20',
        'convert':'USD',
        'sort':'symbol',
    }
    
    # make a request to the coinmarketcap api
    response = requests.get(url, headers=headers, params=parameters)
    response_json = response.json()
    print(response_json)
    # extract the bitcoin price from the json data
    btc_price = response_json['data'][0]
    print(btc_price['quote']['USD']['price'])
    return btc_price['quote']['USD']['price']

# make a request to the coingecko api
def cg_get_btc_price():
    url = gecko_api_url
    response = requests.get(url)
    response_json = response.json()
    btc_price = response_json[0]
    print(btc_price['current_price'])
    return btc_price['current_price']

# make a request to the wazirx api
def wx_get_btc_price():
    url = wazirx_url
    response = requests.get(url)
    response_json = response.json()
    btc_price = response_json['dogeinr']
    # print(btc_price)
    print(btc_price['last'])
    return float(btc_price['last'])

def send_message(chat_id, msg):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={msg}"
    requests.get(url)

def pricer():
    global price_list

    price = wx_get_btc_price()
    price_list.append(price)

    if price > highball:
        send_message(chat_id=chat_id, msg=f'{coin_name} Price Spike Alert: {price}')
    
    if price < lowball:
        send_message(chat_id=chat_id, msg=f'{coin_name} Price Drop Alert: {price}')
    
    get_tweets('@elonmusk')
    send_message(chat_id=chat_id, msg=f'{coin_name} Price : {price}')
    # if len(price_list) >= ping_amount:
    #     send_message(chat_id=chat_id, msg=f'{coin_name} Price List: {price_list}')
    #     price_list = []

def teleg():
    text = get_last_chat_id_and_text(get_updates())
    if text != last_textchat:
        send_message(text, chat_id)
        last_textchat = text
    print(text)

def main():
    global price_list

    price_list = []
    last_textchat = None
    while True:
        #teleg()
        pricer()
        time.sleep(time_interval)

if __name__ == '__main__':
    main()