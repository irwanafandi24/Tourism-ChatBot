from telegram import *
from telegram.ext import *
import wikipedia
import requests
import Constant as keys
import Responses as R

def start_command(update:Update, context:CallbackContext):
    url = 'https://static.vecteezy.com/system/resources/thumbnails/000/242/789/small/jungle-explorers-vector-illustration.jpg'
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
    update.message.reply_text(
        text='Hai.. <b>welcome to Compas Tourism Bot</b>'
             '\nMy name is Cony, your private guide.'
             "\nI will guide you to get your perfect vocation spot. But, what is your name..? (<b><i>I am</i></b> or <b><i>I'm</i></b> ... )",
        parse_mode=ParseMode.HTML
    )

def handle_message(update:Update, context:CallbackContext):
    text = str(update.message.text).lower()
    response = R.message_response(text)
    update.message.reply_text(
        text=response,
        parse_mode=ParseMode.HTML
    )

def error(update:Update, context:CallbackContext):
    update.message.reply_text(
        text='Sorry, Cony Does not understand what you are saying.'
             '\nType <b><i>\help</i></b> and Cony will help you.',
        parse_mode=ParseMode.HTML
    )

def main():
    print('bot started...')
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()

