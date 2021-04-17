
# def set_doge_low(update: Update, context: CallbackContext):
#     keyboard = [
#         [ InlineKeyboardButton("₹30", callback_data='30'), InlineKeyboardButton("₹20", callback_data='20') ], 
#         [ InlineKeyboardButton("₹15", callback_data='15'), InlineKeyboardButton("₹10", callback_data='10') ]]
#     reply_markup = InlineKeyboardMarkup(keyboard)
#     update.message.reply_text('Please choose:', reply_markup=reply_markup)
#     pass

# def doge_low_button(update, context):
#     global doge_low

#     query: CallbackQuery = update.callback_query
#     query.answer()
#     query.edit_message_text(text="Selected option: ₹{}".format(query.data))
#     print('og doge_low: ', doge_low)
#     doge_low = float(query.data)
#     print('new doge_low: ', doge_low)

# def error(update: Update, context: CallbackContext):
#     sys.stderr.write("ERROR: '%s' caused by '%s'" % context.error, update)
#     pass

# def teleg():
#     text = get_last_chat_id_and_text(get_updates())
#     if text != last_textchat:
#         send_message(text, chat_id)
#         last_textchat = text
#     print(text)

# def get_updates():
#     url = url_with_token + "getUpdates"
#     response = requests.get(url)
#     content = response.content.decode("utf8")
#     js = json.loads(content)
#     return js

# def get_last_chat_id_and_text(updates):
#     num_updates = len(updates["result"])
#     last_update = num_updates - 1
#     text = updates["result"][last_update]["message"]["text"]
#     chat_id = updates["result"][last_update]["message"]["chat"]["id"]
#     return text

# # make a request to the coinmarketcap api
# def cm_get_btc_price():
#     url = coin_api_url
#     headers = {
#         'Accepts': 'application/json',
#         'X-CMC_PRO_API_KEY': api_key
#     }
#     parameters = {
#         'start':'1',
#         'limit':'20',
#         'convert':'USD',
#         'sort':'symbol',
#     }
    
#     # make a request to the coinmarketcap api
#     response = requests.get(url, headers=headers, params=parameters)
#     response_json = response.json()
#     print(response_json)
#     # extract the bitcoin price from the json data
#     btc_price = response_json['data'][0]
#     print(btc_price['quote']['USD']['price'])
#     return btc_price['quote']['USD']['price']

# # make a request to the coingecko api
# def cg_get_btc_price():
#     url = gecko_api_url
#     response = requests.get(url)
#     response_json = response.json()
#     btc_price = response_json[0]
#     print(btc_price['current_price'])
#     return btc_price['current_price']