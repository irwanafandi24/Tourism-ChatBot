import re
import math
import Constant as keys
NAME, DESTINATION, DAYS, CURRENT_DAYS, CURRENT_LOCATION, TMP_LOCATION, TMP_PRICE = '', '', 0, 1, '', '', 0
SAVE_DEST, SAVE_RESTO, SAVE_HOTEL, TOTAL_PRICE = [], [], [], []

df = keys.TOURISM_DATA

def message_response(input_text):
    global NAME, DESTINATION, DAYS, CURRENT_LOCATION, SAVE_DEST, SAVE_RESTO, SAVE_HOTEL

    user_message = str(input_text).lower()
    message_split = re.split("[' ]", user_message)

    if user_message.startswith("saya"):
        NAME = (' '.join(message_split[1:])).capitalize()
        reply_text = "Hai "+NAME+"! salam kenal ya.\nSudah tahu mau liburan kemana? Chavel punya rekomendasi nih special buat kamu, <b><i>Mungkin kesini asik</i></b>"
        return reply_text

    if user_message.endswith("hari"):
        DAYS = int(user_message.split()[0])
        react = 'Wah cukup singkat ya hanya'
        if DAYS == 3:
            react = 'Sepertinya mantap nih liburan di '+DESTINATION+' selama'
        if DAYS > 3:
            react = 'Pasti cinta ya sama '+DESTINATION+'? soalnya cukup lama loh'
        reply_text = react+" <b>"+str(DAYS)+" hari</b>.\n\nOky! sekarang Chavel akan bantu kamu nih untuk membuat planning liburan selama di "+DESTINATION+", jadi biar waktumu tidak terbuang sia-sia. Are you ready?"
        return reply_text
    else:
        reply_text = "I'm Sorry, I don't know what you mean "+NAME+" :cry:\nYou can click this word <b><i>/help</i></b>."
        return


def get_sqrt(x):
  return math.sqrt(x)


def shortest_path(df, current_location, place_type):
  df_x = df.copy()
  df_x['distance'] = abs(df_x.latitude**2-float(df_x.loc[df_x.place_name == current_location, 'latitude']**2))+abs(df_x.longitude**2-float(df_x.loc[df_x.place_name == current_location, 'longitude']**2))
  df_x['distance'] = df_x['distance'].apply(get_sqrt)
  df_x = df_x[df_x['type'] == place_type]
  df_x = df_x.sort_values('distance')
  list_place = df_x['place_name'].values
  return list_place[:5]
