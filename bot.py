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
    with open(params.editable_params_filename, "w") as outfile:
        json.dump(params.doge_limits, outfile)

# reply text on command /help
def see_help(update: Update, context: CallbackContext):
    update.message.reply_text(f'get_params: Gives details about coin being tracked like name, price limits and update rate'
        f'set_coin_name: Pick which coin to track'
            f'set_update_rate: Rate at which prices are updated for coin'
                f'set_price_limits: Set upper/lower absolute price limits for coin'
                    f'start_tracker: Start tracking coin prices'
                        f'stop_tracker: Stop tracking coin prices')

# reply text on command /get_params by opening and loading json file data
def get_params(update, context):
    with open(params.editable_params_filename) as jsonFile:
        data = json.load(jsonFile)
        update.message.reply_text(f'coin_name: {data["coin_name"]}\nlimit_low: {data["limit_low"]}\n'
            f'limit_high: {data["limit_high"]}\nupdate_rate: {data["update_rate"]}')
        params.doge_limits = data
        print(f'\nget_params:\nparams.doge_limits: {params.doge_limits}\ndata:\n{data}\n')

# start tracker
def start_tracker(update, context):
    global tracker_subprocess

    with open(params.editable_params_filename) as jsonFile:
        data = json.load(jsonFile)
        params.doge_limits = data

    update.message.reply_text(f'Started tracker for coin')
    tracker_subprocess = subprocess.Popen([sys.executable, params.tracker_filename])
    print(f'Started process: {tracker_subprocess.pid}\n')

# stop tracker
def stop_tracker(update, context):
    global tracker_subprocess
    
    update.message.reply_text(f'Stopped tracker')
    print(f'Killing process: {tracker_subprocess.pid}\n')
    tracker_subprocess.kill()

# reply text on command /set_price_limits and show keyboard options
def set_price_limits(update: Update, _: CallbackContext) -> int:
    reply_keyboard1 = [['upper'], ['lower']]
    update.message.reply_text(f'Pick which limit to edit\n', reply_markup=ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True))
    return UPPERORLOWER

# save selected option from keyboard into global variable and reply text
def upper_lower_button(update: Update, _: CallbackContext) -> int:
    global selected_option
    selected_option = update.message.text
    print(f'upper_lower_button update.message.text: {selected_option}\n\n')
    update.message.reply_text(f'Editing {selected_option} limit\nEnter value for limit\n')
    return UPDATELIMITS

# reply text and change values of limits first for doge_limits dict which is then saved to json file using save_to_json_file()
def price_changer(update: Update, _: CallbackContext) -> int:
    global selected_option
    print(f'selected_option: {selected_option}\n\n')
    print(f'price_changer update.message.text: {update.message.text}\n')
    update.message.reply_text(f'Set limit to ₹{update.message.text}\n')
    if ("upper" == selected_option):
        print(f'og params.doge_limits["limit_high"]: {params.doge_limits["limit_high"]}\n')
        params.doge_limits["limit_high"] = float(update.message.text)
        print(f'updated params.doge_limits["limit_high"]: {params.doge_limits["limit_high"]}\n')
    elif ("lower" == selected_option):
        print(f'og params.doge_limits["limit_low"]: {params.doge_limits["limit_low"]}\n\n')
        params.doge_limits["limit_low"] = float(update.message.text)
        print(f'updated  params.doge_limits["limit_low"]: {params.doge_limits["limit_low"]}\n')
    save_to_json_file()
    return ConversationHandler.END

# on command /set_update_rate show options and reply message
def set_update_rate(update: Update, _: CallbackContext) -> int:
    reply_keyboard2 = [['5'], ['10'], ['15'], ['30'], ['60']]
    update.message.reply_text(f'Pick update rate in seconds\n', reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True))
    return UPDATERATE

# reply to previous choice and change values of update rate first for doge_limits dict which is then saved to json file using save_to_json_file()
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

# reply to previous choice and change values of coin name first for doge_limits dict which is then saved to json file using save_to_json_file()
def coin_name_value(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(f'Coin name updated to {update.message.text}\n')
    params.doge_limits["coin_name"] = update.message.text
    save_to_json_file()
    return ConversationHandler.END

# not used i guess? but still exists as fallback
def cancel(update: Update, _: CallbackContext) -> int:
    update.message.reply_text(f'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove() )
    return ConversationHandler.END

def main():
    global updater, selected_option

    selected_option = None
    
    updater = Updater(params.bot_token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start_tracker', start_tracker))
    dispatcher.add_handler(CommandHandler('stop_tracker', stop_tracker))
    dispatcher.add_handler(CommandHandler('help', see_help))
    dispatcher.add_handler(CommandHandler('get_params', get_params))

    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler('set_price_limits', set_price_limits)],
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
