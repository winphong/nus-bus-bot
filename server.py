import json
import xml.etree.ElementTree as ET
from bot import telegram_chatbot
bot = telegram_chatbot("config.cfg")

def make_reply(msg):
    reply = "okay"
    return reply


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
            reply = bot.get_closest()
            bot.send_message(reply, from_)