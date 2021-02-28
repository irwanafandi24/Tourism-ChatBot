import re
name, location, destination, member, days = '', '', '', 0, 0

def message_response(input_text):
    global name, location, destination, member, days

    user_message = str(input_text).lower()
    message_split = re.split("[' ]", user_message)

    if user_message.startswith("i am") or user_message.startswith("i'm"):
        name = (' '.join(message_split[2:])).capitalize()
        reply_text = "Hai "+name+"! Nice to meet you.\nWhere are you know? (<b><i>In</i></b> ... )"
        return reply_text

    if user_message.startswith("in"):
        location = (' '.join(message_split[1:])).capitalize()
        reply_text = "Ok "+name+", you are from "+location+ ". Where do you want to go? (<b><i>To</i></b> ... )"
        return reply_text

    if user_message.startswith("to"):
        destination = (' '.join(message_split[1:])).capitalize()
        reply_text = "How many people will go to "+destination+"? ( ... <b><i>people</i></b>)"
        return reply_text

    if user_message.endswith("people"):
        member = int(user_message.split()[0])
        reply_text = "How many days will you stay in "+destination+"? ( ... <b><i>days</i></b>)"
        return reply_text

    if user_message.endswith("days"):
        days = int(user_message.split()[0])
        reply_text = "Ok <b><i>"+name+"</i></b>, This is what <b>Cony</b> gets from the data that you have entered.\n\nCurrent Location\t: "+location+"\nDestination\t: "+destination+"\nStayed For\t: "+str(days)+" days\nNumber of members\t: "+str(member)+"\n\nCony will find the best recommendation for you:) <b>Wait a minute...</b>"
        return reply_text
