from pandas.core.computation.ops import BinOp
from telegram import *
from telegram.ext import *
import wikipedia
import requests

bot = Bot('1673987148:AAFthPcXoEQbYYbXeuT05UQ9wVMUzFLHrrY')
print(bot.getMe())

updater = Updater('1673987148:AAFthPcXoEQbYYbXeuT05UQ9wVMUzFLHrrY', use_context=True)
dispatcher : Dispatcher = updater.dispatcher

#empty variable
keyword, chat_id = '', ''

def test1(update:Update, context:CallbackContext):
    bot.send_message(
        chat_id= update.effective_chat.id,
        text='Hai.. <b>welcome to Compas Tourism Bot</b>'
             '\nMy name is Comy, your private guide.'
             '\nI will guide you to get your perfect vocation spot. But, what is your name..?',
        parse_mode= ParseMode.HTML
    )

#show the keyboard botton
def showkeyboard(update:Update, context:CallbackContext):
    #handling input from user
    global keyword, chat_id
    keyword = update.message.text
    chat_id = update.message.chat_id

    #make response button
    keyboard = [[
        InlineKeyboardButton('ABOUT', callback_data='ABOUT'),
        InlineKeyboardButton('IMAGE', callback_data='IMAGE')
    ]]

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)

#button_click
def button_click(update:Update, context:CallbackContext):
    global keyword, chat_id

    query : CallbackQuery = update.callback_query

    if query.data == 'ABOUT':
        summary = wikipedia.summary(keyword)
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=summary,
            parse_mode=ParseMode.HTML
        )

    if query.data == "IMAGE":
        headers = {
            "apikey": "339a68b0-778d-11eb-89b8-23821a7ac784"}

        params = (
            ('q', keyword),
            ('tbm', 'isch'),
        )

        response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params)

        data = response.json()
        first_image = data['image_results'][0]['thumbnail']

        bot.send_photo(chat_id=chat_id, photo=first_image)


# dispatcher.add_handler(MessageHandler(Filters.text, test1))
dispatcher.add_handler(MessageHandler(Filters.text, showkeyboard))

dispatcher.add_handler(CallbackQueryHandler(button_click))

updater.start_polling()

# https://www.youtube.com/watch?v=7qJFtGi0hNQ&ab_channel=Iknowpython
# https://www.codementor.io/@garethdwyer/building-a-telegram-bot-using-python-part-1-goi5fncay