import json
import xml.etree.ElementTree as ET
from bot import telegram_chatbot
bot = telegram_chatbot("config.cfg")

update_id = None
while True:
    updates = bot.get_updates(offset=update_id)
    updates = updates["result"]
    if updates:
        for item in updates:
            update_id = item["update_id"]
            try:
                message = str(item["message"]["text"])
            except: 
                message = None
            from_ = item["message"]["from"]["id"]
            
            try :
                if (message == "/start"):
                    reply = '''Welcome to NUS Bus!\nPlease enter a valid command to retrieve the timing of bus at the specified bus stop e.g. /yih'''
                elif ("/" not in message or len(message) == 1):
                    reply = "Please provide a valid command!"
                elif (message == "/help"):
                    reply = '''Please enter a valid command to retrieve the timing of bus at the specified bus stop e.g. /yih\n
                    More bus stops will be supported soon!'''
                elif (message == "/rhtobiz"):
                    reply = bot.get_rh_to_biz()
                else:
                    reply = bot.get_buses(message[1:].upper())
            except: 
                reply = "Please provide a valid command!"

            bot.send_message(reply, from_)