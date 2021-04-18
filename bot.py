import params
import os
import sys
import json
import signal
import tracker
import subprocess

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import Updater, ConversationHandler, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, Dispatcher
from telegram.callbackquery import CallbackQuery
from telegram.update import Update
from telegram.message import Message

UPPERORLOWER, UPDATELIMITS, UPDATERATE = range(3)

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
            '\ndoge_low: '+str(data["doge_low"])+
                '\ndoge_high: '+str(data["doge_high"])+
                    '\nupdate_rate: '+str(data["update_rate"]))

# start tracker
def start_tracker(update, context):
    global tracker_subprocess
    update.message.reply_text('Started tracker')
    fileDir = os.path.dirname(os.path.realpath('/home/pi/Projects/crypto-notifier/tracker.py'))
    filename = os.path.join(fileDir, 'tracker.py')
    tracker_subprocess = subprocess.Popen([sys.executable, filename])
    # tracker_subprocess = subprocess.Popen([sys.executable, 'tracker.py'], stdout=subprocess.PIPE, shell=True)
    print("Started process: ", tracker_subprocess.pid)
    print('start_tracker tracker_subprocess.poll(): ', tracker_subprocess.poll())

# stop tracker
def stop_tracker(update, context):
    global tracker_subprocess
    update.message.reply_text('Stopped tracker')
    print("Killing process: ", tracker_subprocess.pid)
    tracker_subprocess.kill()
    print('stop_tracker tracker_subprocess.poll(): ', tracker_subprocess.poll())

# send_message() on command /check_params
def set_doge_limits(update: Update, _: CallbackContext) -> int:
    reply_keyboard1 = [['upper'], ['lower']]
    update.message.reply_text('Pick which limit to edit\n', reply_markup=ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True))
    return UPPERORLOWER

def upper_lower_button(update: Update, _: CallbackContext) -> int:
    global selected_option
    selected_option = update.message.text
    print("upper_lower_button update.message.text", update.message.text)
    update.message.reply_text('Editing {} limit\nEnter value for limit\n'.format(update.message.text))
    return UPDATELIMITS

# change values of limits on text
def price_changer(update: Update, _: CallbackContext) -> int:
    global selected_option
    print('selected_option: ', selected_option)
    print("price_changer update.message.text", update.message.text)
    update.message.reply_text('Set limit to ₹{}\n'.format(update.message.text))
    if ("upper" == selected_option):
        print('og params.doge_limits["doge_high"]: ', params.doge_limits["doge_high"])
        params.doge_limits["doge_high"] = float(update.message.text)
        print('updated params.doge_limits["doge_high"]: ',  params.doge_limits["doge_high"])
    elif ("lower" == selected_option):
        print('og params.doge_limits["doge_low"]: ',  params.doge_limits["doge_low"])
        params.doge_limits["doge_low"] = float(update.message.text)
        print('updated  params.doge_limits["doge_low"]: ',  params.doge_limits["doge_low"])
    save_to_json_file()
    return ConversationHandler.END

# send_message() on command /check_params
def set_update_rate(update: Update, _: CallbackContext) -> int:
    reply_keyboard = [['5'], ['10'], ['15'], ['30'], ['60']]
    update.message.reply_text('Pick update rate in seconds\n', reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return UPDATERATE

def update_rate_value(update: Update, _: CallbackContext) -> int:
    # print("update.message.text", update.message.text)
    update.message.reply_text('Update time updated to {} seconds\n'.format(update.message.text))
    params.doge_limits["update_rate"] = float(update.message.text)
    save_to_json_file()
    return ConversationHandler.END

def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text( 'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove() )
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

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
