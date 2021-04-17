import params
import os
import sys
import signal
import tracker
import subprocess

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, ConversationHandler, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, Filters, Dispatcher
from telegram.callbackquery import CallbackQuery
from telegram.update import Update
from telegram.message import Message

# send_message() on command /help
def see_help(update: Update, context: CallbackContext):
    update.message.reply_text('This is your help?')

# send_message() on command /check_params
def check_params(update, context):
    update.message.reply_text('doge_looky: '+str(params.doge_looky)+'\ndoge_low: '+str(params.doge_low)+'\ndoge_high: '+str(params.doge_high))

# start tracker
def start_tracker(update, context):
    global tracker_subprocess
    update.message.reply_text('Started tracker')
    tracker_subprocess = subprocess.Popen([sys.executable, 'tracker.py'])
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
def set_doge_limits(update, context):
    keyboard = [[InlineKeyboardButton("Upper Limit", callback_data='upper'), InlineKeyboardButton("Lower Limit", callback_data='lower') ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    pass

def upper_lower_button(update, context):
    global selected_option
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Selected option: {} limit\nProceed with entering a value for the same".format(query.data))
    selected_option = query.data

# change values of limits on text
def price_changer(update, context):
    global selected_option
    
    print('selected_option: ', selected_option)
    print('update.message.text: ', update.message.text)
    update.message.reply_text('Set '+str(selected_option)+' limit to ₹'+str(float(update.message.text)))
    if ("upper" == selected_option):
        print('og params.doge_high: ', params.doge_high)
        params.doge_high = float(update.message.text)
        print('updated params.doge_high: ', params.doge_high)
    elif ("lower" == selected_option):
        print('og params.doge_low: ', params.doge_low)
        params.doge_low = float(update.message.text)
        print('updated params.doge_low: ', params.doge_low)

def main():
    global updater, selected_option

    selected_option = None
    updater = Updater(params.bot_token, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start_tracker', start_tracker))
    dispatcher.add_handler(CommandHandler('stop_tracker', stop_tracker))
    dispatcher.add_handler(CommandHandler('help', see_help))
    dispatcher.add_handler(CommandHandler('check_params', check_params))
    dispatcher.add_handler(CommandHandler('set_doge_limits', set_doge_limits))
    dispatcher.add_handler(CallbackQueryHandler(upper_lower_button))
    dispatcher.add_handler(MessageHandler(Filters.text, price_changer))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()