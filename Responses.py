import re
name, location, destination, member, days, current_location = '', '', '', 0, 0, ''

def message_response(input_text):
    global name, location, destination, member, days, current_location

    user_message = str(input_text).lower()
    message_split = re.split("[' ]", user_message)

    ##get destination
    if user_message == 'bali':
        destination = 'Bali'

    if user_message.startswith("saya"):
        name = (' '.join(message_split[1:])).capitalize()
        reply_text = "Hai "+name+"! salam kenal ya.\nSudah tahu mau liburan kemana? Chavel punya rekomendasi nih special buat kamu, <b><i>Mungkin kesini asik</i></b>"
        return reply_text

    if user_message.endswith("hari"):
        days = int(user_message.split()[0])
        reply_text = "Biar <b>"+str(days)+" harimu</b> tidak terbuang sia-sia, ayo kita buat planning yang matang. Biasanya orang yang ke "+destination+" itu juga ke:"
        return reply_text

    if user_message.startswith("in"):
        location = (' '.join(message_split[1:])).capitalize()
        reply_text = "Ok "+name+", you are from "+location+ ". Where do you want to go? (<b><i>To</i></b> ... )"
        return reply_text

    if user_message.startswith("to"):
        destination = (' '.join(message_split[1:])).capitalize()
        reply_text = "How many people will go to "+destination+"? ( ... <b><i>people</i></b>)"
        return reply_text

    if user_message.endswith("days"):
        days = int(user_message.split()[0])
        reply_text = "Ok <b><i>"+name+"</i></b>, This is what <b>Cony</b> gets from the data that you have entered.\n\nCurrent Location\t: "+location+"\nDestination\t: "+destination+"\nStayed For\t: "+str(days)+" days\nNumber of members\t: "+str(member)+"\n\nCony will find the best recommendation for you:) <b>Wait a minute...</b>"
        return reply_text
    else:
        reply_text = "I'm Sorry, I don't know what you mean "+name+" :cry:\nYou can click this word <b><i>/help</i></b>."
        return reply_text
