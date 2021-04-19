import params
import os
import sys
import json
import signal
import tracker
import subprocess

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, ConversationHandler, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, Dispatcher
from telegram.callbackquery import CallbackQuery
from telegram.update import Update
from telegram.message import Message

UPPERORLOWER, UPDATELIMITS, UPDATERATE, UPDATECOINNAME = range(4)

# called to open json file and dump params.doge_limits
def save_to_json_file():
    fileDir = os.path.dirname(os.path.realpath('/home/pi/Projects/crypto-notifier/editable_params.json'))
    filename = os.path.join(fileDir, 'editable_params.json')
    with open(filename, "w") as outfile:
        json.dump(params.doge_limits, outfile)

# send_message() on command /help
def see_help(update: Update, context: CallbackContext):
    update.message.reply_text('This is your help?')

# send_message() on command /check_params
def check_params(update, context):
    fileDir = os.path.dirname(os.path.realpath('/home/pi/Projects/crypto-notifier/editable_params.json'))
    filename = os.path.join(fileDir, 'editable_params.json')
    with open(filename) as jsonFile:
        data = json.load(jsonFile)
        update.message.reply_text('coin_looky: '+str(data["coin_looky"])+
            '\nlimit_low: '+str(data["limit_low"])+
                '\nlimit_high: '+str(data["limit_high"])+
                    '\nupdate_rate: '+str(data["update_rate"]))

# start tracker
def start_tracker(update, context):
    global tracker_subprocess
    update.message.reply_text(f'Started tracker')
    fileDir = os.path.dirname(os.path.realpath('/home/pi/Projects/crypto-notifier/tracker.py'))
    filename = os.path.join(fileDir, 'tracker.py')
    tracker_subprocess = subprocess.Popen([sys.executable, filename])
    # tracker_subprocess = subprocess.Popen([sys.executable, 'tracker.py'], stdout=subprocess.PIPE, shell=True)
    print(f'Started process: {tracker_subprocess.pid}')
    print(f'start_tracker tracker_subprocess.poll(): {tracker_subprocess.poll()}')

# stop tracker
def stop_tracker(update, context):
    global tracker_subprocess
    update.message.reply_text(f'Stopped tracker')
    print(f'Killing process: {tracker_subprocess.pid}')
    tracker_subprocess.kill()
    print(f'stop_tracker tracker_subprocess.poll(): {tracker_subprocess.poll()}')

# send_message() on command /check_params
def set_doge_limits(update: Update, _: CallbackContext) -> int:
    reply_keyboard1 = [['upper'], ['lower']]
    update.message.reply_text(f'Pick which limit to edit\n', reply_markup=ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True))
    return UPPERORLOWER

def upper_lower_button(update: Update, _: CallbackContext) -> int:
    global selected_option
    selected_option = update.message.text
    print(f'upper_lower_button update.message.text: {update.message.text}')
    update.message.reply_text(f'Editing {update.message.text} limit\nEnter value for limit\n')
    return UPDATELIMITS

# change values of limits on text
def price_changer(update: Update, _: CallbackContext) -> int:
    global selected_option
    print(f'selected_option: {selected_option}')
    print(f'price_changer update.message.text: {update.message.text}')
    update.message.reply_text(f'Set limit to ₹{update.message.text}\n')
    if ("upper" == selected_option):
        print(f'og params.doge_limits["limit_high"]: {params.doge_limits["limit_high"]}')
        params.doge_limits["limit_high"] = float(update.message.text)
        print(f'updated params.doge_limits["limit_high"]: {params.doge_limits["limit_high"]}')
    elif ("lower" == selected_option):
        print(f'og params.doge_limits["limit_low"]: {params.doge_limits["limit_low"]}')
        params.doge_limits["limit_low"] = float(update.message.text)
        print(f'updated  params.doge_limits["limit_low"]: {params.doge_limits["limit_low"]}')
    save_to_json_file()
    return ConversationHandler.END

# on command /set_update_rate show options and reply message
def set_update_rate(update: Update, _: CallbackContext) -> int:
    reply_keyboard2 = [['5'], ['10'], ['15'], ['30'], ['60']]
    update.message.reply_text(f'Pick update rate in seconds\n', reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
    return UPDATERATE

# reply to previous choice and save the value to params.doge_limits dict and then to save_to_json_file()
def update_rate_value(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(f'Update time updated to {update.message.text} seconds\n')
    params.doge_limits["update_rate"] = float(update.message.text)
    save_to_json_file()
    return ConversationHandler.END

# on command /set_coin_name show options and reply message
def set_coin_name(update: Update, _: CallbackContext) -> int:
    reply_keyboard3 = [['btcinr'], ['ethinr'], ['dogeinr'], ['xrpinr'], ['trxinr'], ['bttinr']]
    update.message.reply_text(f'Pick coin name to track\n', reply_markup=ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True))
    return UPDATECOINNAME

def coin_name_value(update: Update, _: CallbackContext) -> int:
    # print("update.message.text", update.message.text)
    update.message.reply_text(f'Coin name updated to {update.message.text}\n')
    params.doge_limits["coin_looky"] = update.message.text
    save_to_json_file()
    return ConversationHandler.END

def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(f'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove() )
    return ConversationHandler.END

def main():
    global updater, selected_option

    selected_option = None
    fileDir = os.path.dirname(os.path.realpath('/home/pi/Projects/crypto-notifier/editable_params.json'))
    filename = os.path.join(fileDir, 'editable_params.json')
    with open(filename) as jsonFile:
        data = json.load(jsonFile)
        params.doge_limits = data

    updater = Updater(params.bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start_tracker', start_tracker))
    dispatcher.add_handler(CommandHandler('stop_tracker', stop_tracker))
    dispatcher.add_handler(CommandHandler('help', see_help))
    dispatcher.add_handler(CommandHandler('check_params', check_params))

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('set_doge_limits', set_doge_limits)],
        states={UPPERORLOWER: [MessageHandler(Filters.text, upper_lower_button)], 
                UPDATELIMITS: [MessageHandler(Filters.text, price_changer)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler1)
    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('set_update_rate', set_update_rate)],
        states={UPDATERATE: [MessageHandler(Filters.text, update_rate_value)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler2)
    conv_handler3 = ConversationHandler(
        entry_points=[CommandHandler('set_coin_name', set_coin_name)],
        states={UPDATECOINNAME: [MessageHandler(Filters.text, coin_name_value)]},
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conv_handler3)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
