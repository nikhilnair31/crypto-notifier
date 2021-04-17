#!/usr/bin/env python
# pylint: disable=C0116
# This program is dedicated to the public domain under the CC0 license.

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from params import *
from init import *
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    MessageHandler,
    Filters,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
UPPER, LOWER = range(2)


def start_over(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    keyboard = [[InlineKeyboardButton("Upper Limit", callback_data=str(UPPER)), InlineKeyboardButton("Lower Limit", callback_data=str(LOWER)) ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return FIRST

def end(update: Update, _: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="See you next time!")
    return ConversationHandler.END

# send_message() on command /help
def see_help(update: Update, context: CallbackContext):
    update.message.reply_text('This is your help?')

# send_message() on command /check_params
def check_params(update: Update, context: CallbackContext):
    global doge_looky, doge_low, doge_high
    update.message.reply_text('doge_looky: '+str(doge_looky)+'\ndoge_low: '+str(doge_low)+'\ndoge_high: '+str(doge_high))

# send_message() on command /check_params
def set_doge_limits(update, context) -> int:
    keyboard = [[InlineKeyboardButton("Upper Limit", callback_data=str(UPPER)), InlineKeyboardButton("Lower Limit", callback_data=str(LOWER)) ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)
    return FIRST

def upper(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Selected option: {} limit\nProceed with entering a value for the same".format(query.data))
    return FIRST

def lower(update: Update, _: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Selected option: {} limit\nProceed with entering a value for the same".format(query.data))
    return FIRST

# change values of limits on text
def price_changer(update, context):
    global doge_high, doge_low
    
    print('update.message.text: ', update.message.text)
    print('update.callback_query: ', update.callback_query)
    update.message.reply_text('Set '+str(update.callback_query)+' limit to ₹'+str(float(update.message.text)))
    if ("upper" == update.callback_query):
        doge_high = float(update.message.text)
    elif ("lower" == update.callback_query):
        doge_low = float(update.message.text)

def main():
    updater = Updater(bot_token)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('set_doge_limits', set_doge_limits), CommandHandler('check_params', check_params)],
        states={
            FIRST: [
                CallbackQueryHandler(upper, pattern='^' + str(UPPER) + '$'),
                CallbackQueryHandler(lower, pattern='^' + str(LOWER) + '$'),
                MessageHandler(Filters.text, price_changer),
            ],
            SECOND: [
                CallbackQueryHandler(start_over, pattern='^' + str(UPPER) + '$'),
                CallbackQueryHandler(end, pattern='^' + str(LOWER) + '$'),
            ],
        },
        fallbacks=[CommandHandler('help', see_help)],
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()