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
                     \nPanggil saja kami <b><i>Chavel</i></b>, disini kami akan memandu anda untuk keliling Indonesia. Upss sabar, tak kenal maka tak sayang. Yuk kenalan dulu, siapa namamu..? (<b><i>saya</i></b> ... )",
        parse_mode=ParseMode.HTML
    )

def help_command(update:Update, context:CallbackContext):
    update.message.reply_text(
        text="<b><i>/start</i></b> : to start the bot\n<b><i>/vocation</i></b> : show all possible vocation\n<b><i>/food </i></b> : show all restourant near you",
        parse_mode=ParseMode.HTML
    )


def handle_message(update: Update, context: CallbackContext):
    text = str(update.message.text).lower()
    print(text)
    response = R.message_response(text)

    if text.startswith("saya") or text == "no, i'm not ready":
        keyboard1 = [[
            InlineKeyboardButton('Bali', callback_data='BALI'),
            InlineKeyboardButton('NTT', callback_data='NTT'),
            InlineKeyboardButton('NTB', callback_data='NTB'),
            ],
            [
            InlineKeyboardButton('Yogyakarta', callback_data='YGY'),
            InlineKeyboardButton('Sumatera Utara', callback_data='SUMUT')
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
        response = "Dihari <b>ke-"+str(R.CURRENT_DAYS)+"</b> Chavel punya rekomendasi tempat-tempat di <b>"+R.DESTINATION.title()+"</b> yang paling sering dikunjungi wisatawan. Kira-kira kamu mau pergi kemana dulu?"
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
            response = get_data['info'].values[0]+". Adapun detail dari tempat wisata tersebut: \n\n<b>Open</b> : " +get_data['time'].values[0] + "\n<b>Price</b> : Rp "+str(int(get_data['price'].values[0]))+" / orang\n<b>Telpon</b> : (+62) "+str(int(get_data['no_telp'].values[0]))+"\n<b>Address</b> : "+get_data['address'].values[0]+"\n<b>No. CHSE</b> : "+get_data['no_chse'].values[0]+"\n\nApakah anda tertarik mengunjungi destinasi tersebut?"
            menu_keyboard = [['Save Destination'], ['Lihat Lainnya']]
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        elif get_data['type'].values[0] == "resto":
            response = get_data['info'].values[0] + ". Adapun detail dari Restaurant ini adalah: \n\n<b>Open</b> : " +get_data['time'].values[0] + "\n<b>Price</b> : Rp " + str(int(get_data['price'].values[0])) + " / porsi\n<b>Telpon</b> : (+62) "+str(int(get_data['no_telp'].values[0]))+"\n<b>Address</b> : " + get_data['address'].values[0] + "\n<b>No. CHSE</b> : "+get_data['no_chse'].values[0]+"\n\nApakah anda tertarik untuk makan disini?"
            menu_keyboard = [['Save Restaurant'], ['Lihat Lainnya']]
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        elif get_data['type'].values[0] == "hotel":
            response = get_data['info'].values[0] + ". Berikut ini detail dari hotel tersebut: \n\n<b>Open</b> : " +get_data['time'].values[0] + "\n<b>Price</b> : Rp " + str(int(get_data['price'].values[0])) + " / malam\n<b>Telpon</b> : (+62) "+str(int(get_data['no_telp'].values[0]))+"\n<b>Address</b> : " + get_data['address'].values[0] + "\n<b>No. CHSE</b> : "+get_data['no_chse'].values[0]+"\n\nApakah anda tertarik menginap di hotel tersebut?"
            menu_keyboard = [['Save Hotel'], ['Lihat Lainnya']]
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)

        R.GET_TYPE = get_data['type'].values[0]
        R.TMP_LOCATION = text
        R.TMP_PRICE = int(get_data['price'].values[0])
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=get_data.image_url.values[0], caption=response,
                               reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text == "lihat lainnya":
        if R.GET_TYPE == "place":
            if R.CURRENT_DAYS == 1:
                menu_keyboard = []
                for destination in keys.DATA_FILTER.loc[keys.DATA_FILTER['flag'] == 1, 'place_name'].values:
                    tmp = []
                    tmp.append(destination.title())
                    menu_keyboard.append(tmp)
            else:
                place_recommendation = R.shortest_path(keys.DATA_FILTER, R.CURRENT_LOCATION, 'place')
                menu_keyboard = []
                for place in place_recommendation:
                    if place not in R.SAVE_DEST:
                        tmp = []
                        tmp.append(place.title())
                        menu_keyboard.append(tmp)
            response = "<b>Dihari ke-" + str(R.CURRENT_DAYS) + "</b>, Chavel hanya punya rekomenda tempat-temapt di bawah ini. Kira-kira kamu mau pergi kemana dulu?"

        elif R.GET_TYPE == "resto":
            resto_recommendation = R.shortest_path(keys.DATA_FILTER, R.CURRENT_LOCATION, 'resto')
            menu_keyboard = []
            for resto in resto_recommendation:
                if resto not in R.SAVE_RESTO:
                    tmp = []
                    tmp.append(resto.title())
                    menu_keyboard.append(tmp)
            response = "Belum cocok dengan restaurant sebelumnya ya? Rekomendasi Chavel untuk <b><i>restaurant yang paling dekat</i></b> dengan <b>"+R.CURRENT_LOCATION.title()+"</b> antara lain:"

        elif R.GET_TYPE == "hotel":
            hotel_recommendation = R.shortest_path(keys.DATA_FILTER, R.CURRENT_LOCATION, 'hotel')
            menu_keyboard = []
            for hotel in hotel_recommendation:
                if hotel not in R.SAVE_HOTEL:
                    tmp = []
                    tmp.append(hotel.title())
                    menu_keyboard.append(tmp)

            response = "Belum cocok dengan hotel sebelumnya ya? Rekomendasi Chavel untuk hotel yang paling dekat dengan <b>" + R.CURRENT_LOCATION.title()+ "</b> antara lain:"

        menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response,
                                 reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text == "save destination":
        R.SAVE_DEST.append(R.TMP_LOCATION)
        R.CURRENT_LOCATION = R.TMP_LOCATION
        R.TOTAL_PRICE.append(R.TMP_PRICE)

        response_choice = [
            "Setelah capek bermain dan jalan-jalan di <b>"+R.CURRENT_LOCATION.title()+"</b> Yuk isi tenaga dulu. Berikut <b><i>rekomendasi restaurant</i></b> yang paling dekat dengan lokasi anda sekarang:",
            "Lama bermain perut pasti keroncongan, yuk makan dulu. Lokasinya <b><i>restaurannya tidak jauh</i></b> kok, mana pilihanmu?",
            "Habis bersenang-senang di <b>"+R.CURRENT_LOCATION.title()+"</b> tidak lengkap rasanya kalau belum makan di daerah sana juga. Yuk pilih <b><i>rekomendasi restaurant</i></b> yang sesuai dengan seleramu: "
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
        R.SAVE_RESTO.append(R.TMP_LOCATION)
        R.CURRENT_LOCATION = R.TMP_LOCATION
        R.TOTAL_PRICE.append(R.TMP_PRICE)

        response_choice = [
            "Untuk liburan <b><i>hari ke-"+str(R.CURRENT_DAYS)+"</i></b> ini kamu ingin menginap dimana? Lokasinya tidak terlalu jauh kok dari <b><i>"+R.CURRENT_LOCATION.title()+"</i></b>.",
            "Setelah seharian jalan-jalan <b>dihari ke-"+str(R.CURRENT_DAYS)+"</b> ini, pasti kamu capek dan ingin istirahat kan? Nah Chavel punya <b><i>rekomendasi hotel terdekat</i></b> nih dari <b><i>"+R.CURRENT_LOCATION.title()+"</i></b>, kira-kira ingin menginap dimana?"
        ]

        hotel_recommendation = R.shortest_path(keys.DATA_FILTER, R.CURRENT_LOCATION, 'hotel')
        menu_keyboard = []
        for hotel in hotel_recommendation:
            if hotel not in R.SAVE_HOTEL:
                tmp = []
                tmp.append(hotel.title())
                menu_keyboard.append(tmp)

        menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
        context.bot.send_message(chat_id=update.effective_chat.id, text=response_choice[randint(0, 1)],
                                 reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text == "save hotel":
        R.SAVE_HOTEL.append(R.TMP_LOCATION)
        R.CURRENT_LOCATION = R.TMP_LOCATION
        R.TOTAL_PRICE.append(R.TMP_PRICE)
        R.CURRENT_DAYS +=1

        response_choice = [
            "Yay, ini <b><i>hari ke-"+str(R.CURRENT_DAYS)+"</i></b> kamu berada di <b>"+R.DESTINATION.title()+"</b>. \n\nTanpa basa-basi lagi, Chavel akan rekomendasi destinasi tempat wisata yang dekat dengan <b><i>"+R.CURRENT_LOCATION.title()+"</i></b>. Tempat mana nih yang ingin kamu kunjungi?",
            "<b>Hari ke-"+str(R.CURRENT_DAYS)+"</b> sudah menantimu, sudah siap untuk jalan-jalan lagi di <b>"+R.DESTINATION.title()+"</b>?\n\nRekomendasi destinasi wisata dari Chavel untuk yang paling dekat dari <b><i> "+R.CURRENT_LOCATION.title()+"</i></b> adalah: "
        ]

        if R.DAYS - R.CURRENT_DAYS != -1:
            place_recommendation = R.shortest_path(keys.DATA_FILTER, R.CURRENT_LOCATION, 'place')
            menu_keyboard = []
            for place in place_recommendation:
                if place not in R.SAVE_DEST:
                    tmp = []
                    tmp.append(place.title())
                    menu_keyboard.append(tmp)

            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)
            context.bot.send_message(chat_id=update.effective_chat.id, text=response_choice[randint(0,1)],
                                     reply_markup=menu_markup, parse_mode=ParseMode.HTML)
        else:
            url = "https://asset.kompas.com/crops/ev_AV76tE2Q7TcSFohsFjBsYQN0=/0x0:999x666/750x500/data/photo/2020/05/26/5eccc5ee7f998.jpg"
            response = "Akhirnya selesai ya planning kita <b>" + R.NAME.title() + "</b>! \nBerikut ini <b>Chavel</b> bantu rekap semua destinasi wisata, restaurant dan hotel yang akan kamu kunjungi selama di <b>" + R.DESTINATION.title() + "</b> dalam waktu <b>" + str(R.DAYS) + " hari</b>.\n\n"
            data = ""
            for i in range(len(R.SAVE_DEST)):
                data += "<b>~ Hari ke-" + str(i + 1) + "</b> anda akan ke\n"
                data += "Destinasi Wisata  : " + str(R.SAVE_DEST[i]).title() + "\n"
                data += "Restaurant            : " + str(R.SAVE_RESTO[i]).title() + "\n"
                data += "Hotel                       : " + str(R.SAVE_HOTEL[i]).title() + "\n\n"
            data += "Adapun total pengeluaran yang harus anda bayar dalam trip ini sebesar <b>Rp " + str(sum(R.TOTAL_PRICE)) + "</b>. Tapi ingat, ini belum termasuk biaya transportasi ya, jadi semakin banyak tabunganmu maka akan semakin aman :D\n\nSemoga liburanmu menyenangkan ya <b>" + R.NAME.title() + "</b>\nJangan lupain <b>Chavel</b> ya kalau sudah senang di <b>"+R.DESTINATION.title()+"</b>."
            response += data
            menu_keyboard = [['Chavel Selalu di Hati'], ['Ah Biasa Aja']]
            menu_markup = ReplyKeyboardMarkup(menu_keyboard, one_time_keyboard=True, resize_keyboard=True)

            context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=response,
                                   reply_markup=menu_markup, parse_mode=ParseMode.HTML)

    elif text == "chavel selalu di hati":
        url = 'https://www.marbellaweddingangels.com/wp-content/uploads/2017/05/love-valentines-day-79@1x.jpg'
        response = 'Ih... so sweet banget sih kamu <b>'+R.NAME.title()+ '</b>. Nanti kalau butuh bantuan <b>Chavel</b> lagi, bisa langsung hubungi Chavel ya. Jangan sungkan-sungkan...'
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=response,
                                parse_mode=ParseMode.HTML)

    elif text == "ah biasa aja":
        url = 'https://image-cdn.medkomtek.com/xpS5VPhzlPT8zMNHuU9b3UihAGo=/1200x675/smart/klikdokter-media-buckets/medias/2310014/original/099939900_1576591774-Tanda-tanda-Anda-sedang-Membesarkan-Anak-Pemarah-Shutterstock_1034366974.jpg'
        response = 'Jadi <b>Chavel</b> gak selalu di hatinya <b>' + R.NAME.title() + '</b> ya? Yaudah sih, aku ngak akan sedih juga. Tapi kapan-kapan kunjungi Chavel lagi ya.'
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=response,
                               parse_mode=ParseMode.HTML)
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
        R.DESTINATION = 'bali'
        keys.DATA_FILTER = df[df.destination == 'bali']
        url = 'https://www.korinatour.co.id/wp-content/uploads/2018/12/6-300x300.png'
        text = "<b>~Welcome to Bali~</b>\n\nSaya suka dengan selera anda :D\
                    \nBerkunjung ke <b>Pulaunya Para Dewa</b> memang memberikan kesan tersendiri. Kamu akan dimanjakan dengan keindahan alam, kuliner dan juga adat istiadatnya. Gak sabar kan? Sabar ya Chavel mau tanya nih, berapa hari kamu akan liburan di <b>"+R.DESTINATION.title()+"</b>? (... <b><i>hari</i></b>)"

    elif query.data == 'NTT':
        R.DESTINATION = 'nusa tenggara timur'
        keys.DATA_FILTER = df[df.destination == 'nusa tenggara timur']
        url = 'https://1.bp.blogspot.com/-qvcsqnys-tY/X5x54tckXTI/AAAAAAAACmk/G5s58RPxav8iZ6ZC1oCPm9pE4SurTp7EgCLcBGAsYHQ/w1200-h630-p-k-no-nu/Pulau%2BKomodo%2Bdi%2BNTT.jpg'
        text = "<b>~Welcome to NTT~</b>\n\nDestinasi yang tepat!\
                            \nNusa Tenggara Timur yang dinobatkan sebagai destinasi terbaik di dunia akan mengejutkanmu dengan sejuta keindahannya! Pantai yang menyegarkan, adat budaya, dan keindahan laut yang memukau bagaikan surga. Gak sabar kan? Sabar ya Chavel mau tanya nih, berapa hari kamu akan liburan di <b>" + R.DESTINATION.title() + "</b>? (... <b><i>hari</i></b>)"

    elif query.data == 'NTB':
        R.DESTINATION = 'nusa tenggara barat'
        keys.DATA_FILTER = df[df.destination == 'nusa tenggara barat']
        url = 'https://modernclassics.info/great_landscapes/Sameti-Beach.jpg'
        text = "<b>~Welcome to NTB~</b>\n\nTepat sekali!\
                            \nTerkenal dengan pantai nya yang begitu eksotis, spot wisata yang sangat indah, dan pemandangan malamnya yang penuh bintang, siapa yang dapat menolak keindahan seperti ini? Nusa Tenggara Barat akan menyambutmu dengan pemandangan dan pengalaman yang mengagumkan! Gak sabar kan? Sabar ya Chavel mau tanya nih, berapa hari kamu akan liburan di <b>" + R.DESTINATION.title() + "</b>? (... <b><i>hari</i></b>)"

    elif query.data == 'YGY':
        R.DESTINATION = 'yogyakarta'
        keys.DATA_FILTER = df[df.destination == 'yogyakarta']
        url = 'https://i.pinimg.com/736x/84/35/a6/8435a64ae7485477840c109390847169.jpg'
        text = "<b>~Welcome to Yogyakarta~</b>\n\nHemm Menarik!\
                            \nIni nih destinasi yang sering disebut kota wisata paling menarik di Indonesia! Selalu memberikan kenangan yang indah bagi pengunjungnya. Kota yang kaya akan seni dan sejarah! Gak sabar kan? Sabar ya Chavel mau tanya nih, berapa hari kamu akan liburan di <b>" + R.DESTINATION.title() + "</b>? (... <b><i>hari</i></b>)"

    elif query.data == 'SUMUT':
        R.DESTINATION = 'sumatera utara'
        keys.DATA_FILTER = df[df.destination == 'sumatera utara']
        url = 'https://1.bp.blogspot.com/-Yb33hzlDQu0/XmRdrcjgTCI/AAAAAAAAH3c/ESvmIie09cgUXutFNVv5ClFAEVcqtPpXwCLcBGAsYHQ/s640/toba1.jpeg'
        text = "<b>~Welcome to Sumatera Utara~</b>\n\nKeren! Destinasi ini memang tidak boleh dipandang sebelah mata.\
                            \nSumatera Utara dengan berbagai tempat wisatanya yang menyimpan sejuta pesona, apa pun yang kamu cari bisa kamu dapat disana. Masing-masing wisata juga memiliki kisah dan keunikan tersendiri loh. Gak sabar kan? Sabar ya Chavel mau tanya nih, berapa hari kamu akan liburan di <b>" + R.DESTINATION.title() + "</b>? (... <b><i>hari</i></b>)"

    context.bot.send_photo(chat_id=update.effective_chat.id, photo=url, caption=text,
                           parse_mode=ParseMode.HTML)

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

