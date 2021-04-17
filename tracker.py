from params import *
from init import *

import sys
import tweepy
import requests
import time
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, Dispatcher
from telegram.callbackquery import CallbackQuery
from telegram.update import Update
from telegram.message import Message

# Function to extract tweets
def get_tweets(username):
    global last_made_tweet, check_coin_in_tweet
    for status in tweepy.Cursor(api.user_timeline, screen_name=username, count=None, since_id=None, max_id=None, trim_user=True, exclude_replies=True, contributor_details=False, include_entities=False).items(number_of_tweets):
        print(status.text+"\n")
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
    print(doge_price['last'])
    return float(doge_price['last'])

# message from bot to user
def send_message(chat_id, msg):
    url = 'https://api.telegram.org/bot'+bot_token+'/sendMessage?chat_id='+chat_id+'&text='+msg
    requests.get(url)

# compare prices with limits
def pricer():
    doge_price = wx_get_btc_price(doge_looky)

    if doge_price > doge_high:
        send_message(chat_id=chat_id, msg='DOGE Price Spike Alert: '+ str(doge_price))
    if doge_price < doge_low:
        send_message(chat_id=chat_id, msg='DOGE Price Drop Alert: '+ str(doge_price))
    
    get_tweets(user_name)

# send_message() on command /help
def see_help(update: Update, context: CallbackContext):
    send_message(chat_id=chat_id, msg= 'This is your help?')

# send_message() on command /check_params
def check_params(update: Update, context: CallbackContext):
    global doge_looky, doge_low, doge_high
    send_message(chat_id=chat_id, msg= 'doge_looky: '+str(doge_looky)+'\ndoge_low: '+str(doge_low)+'\ndoge_high: '+str(doge_high))

# send_message() on command /check_params
def set_doge_limits(update, context):
    command = context.args[0].lower()
    print('command: ', command)
    context.user_data[set_doge_limits] = command
    if("upper" == command):
        send_message(chat_id=chat_id, msg= "Selected upper limit\nType upper limit amount")
    elif("lower" == command):
        send_message(chat_id=chat_id, msg= "Selected lower limit\nType lower limit amount")

# change values of limits on text
def price_changer(update, context):
    global doge_high, doge_low
    print('context.user_data[set_doge_limits]: ',context.user_data[set_doge_limits])
    send_message(chat_id=chat_id, msg= 'Set '+str(context.user_data[set_doge_limits])+' limit to ₹'+str(float(update.message.text)))
    if ("upper" == context.user_data[set_doge_limits]):
        doge_high = float(update.message.text)
    elif ("lower" == context.user_data[set_doge_limits]):
        doge_low = float(update.message.text)

def main():
    global updater
    last_textchat = None

    updater = Updater(bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('help', see_help))
    dispatcher.add_handler(CommandHandler('check_params', check_params))
    dispatcher.add_handler(CommandHandler('set_doge_limits', set_doge_limits))
    dispatcher.add_handler(MessageHandler(Filters.text, price_changer))
    updater.start_polling()
    # updater.idle()

    while True:
        pricer()
        time.sleep(time_interval)

if __name__ == '__main__':
    main()