import json
import requests
import xml.etree.ElementTree as ET
import os
from bot import telegram_chatbot

bot = telegram_chatbot()

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
                    reply = '''Enter a valid command to retrieve the timing of bus at the specified bus stop e.g. /yih\n\nMore bus stops will be supported soon!'''
                elif (message == "/rhtobiz"):
                    reply = bot.get_rh_to_biz()
                elif (message == "/rhtosci"):
                    reply = bot.get_rh_to_sci()
                else:
                    reply = bot.get_buses(message[1:].upper())
            except requests.exceptions.RequestException: 
                reply = "It appears that the server is not responding. Please try again later.\n\nSorry for the inconvenience caused!"
            except:
                reply = "Error!!"

            bot.send_message(reply, from_)