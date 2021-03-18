from telegram import *
from telegram.ext import *
from telegram import ReplyKeyboardMarkup
import wikipedia
import requests
import Constant as keys
import Responses as R


def start_command(update:Update, context:CallbackContext):
    url = 'https://cdn1.vectorstock.com/i/thumb-large/47/45/cartoon-comical-character-bali-kids-vector-34684745.jpg'
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=url)
    update.message.reply_text(
        text="Hai..!! <b>welcome to ChavellBot </b>\
                     \nPanggil saja kami <b><i>Chavel</i></b>, disini kami akan memandu anda untuk keliling Indonesia.\
                     \nUpss sabar, tak kenal maka tak sayang. Yuk kenalan dulu, siapa namamu..? (<b><i>saya</i></b> ... )",
        parse_mode=ParseMode.HTML
    )

def help_command(update:Update, context:CallbackContext):
    update.message.reply_text(
        text="<b><i>/start</i></b> : to start the bot\n<b><i>/vocation</i></b> : show all possible vocation\n<b><i>/food </i></b> : show all restourant near you",
        parse_mode=ParseMode.HTML
    )


def handle_message(update:Update, context:CallbackContext):
    text = str(update.message.text).lower()
    print(text)
    response = R.message_response(text)
    if text.startswith("saya"):
        keyboard1 = [[
            InlineKeyboardButton('Bali', callback_data='BALI'),
            InlineKeyboardButton('Danau Toba', callback_data='DNTOBA'),
            InlineKeyboardButton('Yogyakarta', callback_data='YGY'),
            ],
            [
            InlineKeyboardButton('Labuan Bajo', callback_data='LABBJO'),
            InlineKeyboardButton('Likupang', callback_data='LKP'),
            InlineKeyboardButton('Mandalika', callback_data='MDL')
         ]]
        vocation_markup = InlineKeyboardMarkup(keyboard1, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                 reply_markup=vocation_markup, parse_mode=ParseMode.HTML)
    elif text.endswith("hari"):
        menu_keyboard = [['Pantai Sanur'], ['Bedugul'], ['Pantai Kuta']]
        menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                 reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    else:
        response = R.message_response(text)
        update.message.reply_text(
            text=response,
            parse_mode=ParseMode.HTML
        )

    # if text.startswith("in"):
    #     # holiday_url = 'https://commonslibrary.parliament.uk/content/uploads/2019/03/holiday-2103171_1920-1860x1280.jpg'
    #     # keyboard1 = [[
    #     #     InlineKeyboardButton('Bali', callback_data='BALI'),
    #     #     InlineKeyboardButton('Danau Toba', callback_data='DNTOBA'),
    #     #     InlineKeyboardButton('Yogyakarta', callback_data='YGY'),
    #     #     ],
    #     #     [
    #     #     InlineKeyboardButton('Labuan Bajo', callback_data='LABBJO'),
    #     #     InlineKeyboardButton('Likupang', callback_data='LKP'),
    #     #     InlineKeyboardButton('Mandalika', callback_data='MDL')
    #     # ]]
    #     #
    #     # reply_markup1 = InlineKeyboardMarkup(keyboard1, resize_keyboard=True)
    #     # context.bot.send_photo(chat_id=update.effective_chat.id, photo=holiday_url, caption="Where do you want to go?", reply_markup=reply_markup1)
    #
    #     menu_keyboard = [['MenuItem1'], ['MenuItem2']]
    #     menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
    #
    #     context.bot.send_message(chat_id=update.effective_chat.id, text="Where do you want to go?", reply_markup=menu_markup)
    #
    # else:
    #     response = R.message_response(text)
    #     update.message.reply_text(
    #         text=response,
    #         parse_mode=ParseMode.HTML
    #     )

def button_click(update:Update, context:CallbackContext):
    query: CallbackQuery = update.callback_query

    if query.data == 'BALI':
        response = R.message_response('Bali')
        url_bali = 'https://www.korinatour.co.id/wp-content/uploads/2018/12/6-300x300.png'
        text_bali = "Saya suka dengan selera anda :D\
                    \n\nBerkunjung ke <b>Pulaunya para Dewa</b> memang memberikan kesan tersendiri.Kamu akan dimajakan dengan keindahan alam, kuliner dan juga adat istiadatnya. Gak sabar kan? Sabar ya Chavel mau tanya nih, berapa hari kamu akan liburan di Bali? (... <b><i>hari</i></b>)"
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url_bali, caption=text_bali, parse_mode=ParseMode.HTML)

def error(update:Update, context:CallbackContext):
    update.message.reply_text(
        text="Sorry, Cony Does not understand what you are saying.\
             \nType <b><i>\help</i></b> and Cony will help you.",
        parse_mode=ParseMode.HTML
    )


def main():
    print('bot started...')
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_command))
    dp.add_handler(CommandHandler("help", help_command))

    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.add_handler(CallbackQueryHandler(button_click))

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()

