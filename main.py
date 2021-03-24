from telegram import *
from telegram.ext import *
from telegram import ReplyKeyboardMarkup
from random import randint
import wikipedia
import requests
import Constant as keys
import Responses as R

#data destination
df = keys.TOURISM_DATA

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

    if text.startswith("saya") or text == "no, i'm not ready":
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

        if text == "no, i'm not ready":
            response = "Apakah belum cocok dengan destinasi sebelumnya? Mau coba pilih yang lain?\n"
            context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                     reply_markup=vocation_markup, parse_mode=ParseMode.HTML)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                     reply_markup=vocation_markup, parse_mode=ParseMode.HTML)

    elif text.endswith("hari"):
        menu_keyboard = [["Yes, I'm ready"], ["No, I'm not ready"]]
        menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                 reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text == "yes, i'm ready":
        response = "Dihari <b>ke-"+str(R.CURRENT_DAYS)+"</b> Chavel punya rekomendasi tempat-tempat di "+R.DESTINATION+" yang paling sering dikunjungi wisatawan. Kira-kira kamu mau pergi kemana dulu?"
        menu_keyboard = []
        for destination in keys.DATA_FILTER.loc[keys.DATA_FILTER['flag'] == 1, 'place_name'].values:
            tmp = []
            tmp.append(destination.title())
            menu_keyboard.append(tmp)

        menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                 reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text in keys.DATA_FILTER['place_name'].values:
        print("masuk opption ", text)
        get_data = keys.DATA_FILTER[keys.DATA_FILTER.place_name == text]

        if get_data['type'].values[0] == "place":
            response = get_data['info'].values[0]+". Adapun detail dari tempat wisata tersebut: \n\n<b>Open</b>: "+get_data['time'].values[0]+"\n<b>Price</b>: Rp "+str(int(get_data['price'].values[0]))+"\n<b>Address</b>: "+get_data['address'].values[0]+"\n\nApakah anda tertarik mengunjungi destinasi tersebut?"

            menu_keyboard = [['Save Destination'], ['Lihat Destinasi Lain']]
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        elif get_data['type'].values[0] == "resto":
            response = get_data['info'].values[0] + ". Adapun detail dari Restaurant ini adalah: \n\n<b>Open</b>: " +get_data['time'].values[0] + "\n<b>Price</b>: Rp " + str(int(get_data['price'].values[0])) + "\n<b>Address</b>: " + get_data['address'].values[0] + "\n\nApakah anda tertarik untuk makan disini?"

            menu_keyboard = [['Save Restaurant'], ['Lihat Restaurant Lain']]
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        elif get_data['type'].values[0] == "hotel":
            response = get_data['info'].values[0] + ". Berikut ini detail dari hotel tersebut: \n\n<b>Open</b>: " +get_data['time'].values[0] + "\n<b>Price</b>: Rp " + str(int(get_data['price'].values[0])) + "\n<b>Address</b>: " + get_data['address'].values[0] + "\n\nApakah anda tertarik menginap di hotel tersebut?"

            menu_keyboard = [['Save Hotel'], ['Lihat Hotel Lain']]
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)

        R.TMP_LOCATION = text
        R.TMP_PRICE = int(get_data['price'].values[0])
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=get_data.image_url.values[0], caption=response,
                               reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text == "lihat destinasi lain":
        if R.CURRENT_DAYS == 1:
            response = "Dihari ke-" + str(R.CURRENT_DAYS) + ", Chavel hanya punya rekomenda tempat-temapt di bawah ini. Kira-kira kamu mau pergi kemana dulu?"
            menu_keyboard = []
            for destination in keys.DATA_FILTER.loc[keys.DATA_FILTER['flag'] == 1, 'place_name'].values:
                tmp = []
                tmp.append(destination.title())
                menu_keyboard.append(tmp)

            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
            context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                     reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text == "lihat restaurant lain":
        resto_recommendation = R.shortest_path(keys.DATA_FILTER, R.CURRENT_LOCATION, 'resto')
        menu_keyboard = []
        for resto in resto_recommendation:
            if resto not in R.SAVE_RESTO:
                tmp = []
                tmp.append(resto.title())
                menu_keyboard.append(tmp)
        response = "Belum cocok dengan restaurant sebelumnya ya? Rekomendasi Chavel untuk restaurant yang paling dekat dengan "+R.CURRENT_LOCATION+" antara lain:"
        menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                 reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text == "save destination":
        R.SAVE_DEST.append(R.TMP_LOCATION)
        R.CURRENT_LOCATION = R.TMP_LOCATION
        R.TOTAL_PRICE.append(R.TMP_PRICE)

        response_choice = [
            "Setelah capek bermain dan jalan-jalan di <b>"+R.CURRENT_LOCATION.title()+"</b> Yuk isi tenaga dulu. Berikut tempat rekomendasi yang paling dekat dengan lokasi anda sekarang:",
            "Lama bermain perut pasti keroncongan, yuk makan dulu. Lokasinya gak jauh kok, mana pilihanmu?",
            "Habis bersenang-senang di <b>"+R.CURRENT_LOCATION.title()+"</b> tidak lengkap rasanya kalau belum makan di daerah sana juga. Yuk pilih tempat makan seleramu: "
        ]

        resto_recommendation = R.shortest_path(keys.DATA_FILTER, R.CURRENT_LOCATION, 'resto')
        menu_keyboard = []
        for resto in resto_recommendation:
            if resto not in R.SAVE_RESTO:
                tmp = []
                tmp.append(resto.title())
                menu_keyboard.append(tmp)

        menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response_choice[randint(0,2)],
                                 reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text == "save restaurant":
        R.SAVE_HOTEL.append(R.TMP_LOCATION)
        R.CURRENT_LOCATION = R.TMP_LOCATION
        R.TOTAL_PRICE.append(R.TMP_PRICE)

        response_choice = [
            "Untuk hari ke-"+str(R.CURRENT_DAYS)+" ini kamu ingin menginap dimana?",
            "Hari ini pasti kamu capek dan ingin istirahat kan. Nah kira-kira ingin bermalam dimana nih?"
        ]

        hotel_recommendation = R.shortest_path(keys.DATA_FILTER, R.CURRENT_LOCATION, 'hotel')
        menu_keyboard = []
        for hotel in hotel_recommendation:
            if hotel not in R.SAVE_RESTO:
                tmp = []
                tmp.append(hotel.title())
                menu_keyboard.append(tmp)

        menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response_choice[randint(0,1)],
                                 reply_markup=menu_markup, parse_mode=ParseMode.HTML)


    else:
        response = R.message_response(text)
        update.message.reply_text(
            text=response,
            parse_mode=ParseMode.HTML
        )

def button_click(update:Update, context:CallbackContext):
    query: CallbackQuery = update.callback_query
    print('Choose Place Option')
    if query.data == 'BALI':
        R.DESTINATION = 'Bali'
        keys.DATA_FILTER = df[df.destination == 'bali']
        url_bali = 'https://www.korinatour.co.id/wp-content/uploads/2018/12/6-300x300.png'
        text_bali = "Saya suka dengan selera anda :D\
                    \n\nBerkunjung ke <b>Pulaunya para Dewa</b> memang memberikan kesan tersendiri.Kamu akan dimajakan dengan keindahan alam, kuliner dan juga adat istiadatnya. Gak sabar kan? Sabar ya Chavel mau tanya nih, berapa hari kamu akan liburan di Bali? (... <b><i>hari</i></b>)"
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url_bali, caption=text_bali, parse_mode=ParseMode.HTML)

    if query.data == 'DNTOBA':
        print("tobango")

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

    # if(len(R.SAVE_DEST)==len(R.SAVE_HOTEL)==len(R.SAVE_RESTO)==R.DAYS==R.CURRENT_DAYS):
    #     print("DONE")

    dp.add_error_handler(error)

    updater.start_polling()
    updater.idle()

main()

