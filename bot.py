import requests
import json
# import configparser as cfg
import xml.etree.ElementTree as ET
import os


class telegram_chatbot():
    def __init__(self):
        self.token = self.read_token_from_env()
        self.base = "https://api.telegram.org/bot{}/".format(self.token)

    def get_updates(self, offset=None):
        url = self.base + "getUpdates"
        if offset: # if offset specified, append offset to param
            url = url + "?offset={}&timeout=100".format(offset + 1)
        r = requests.get(url)
        return json.loads(r.content)

    def send_message(self, msg, chat_id):
        url = self.base + "sendMessage?chat_id={}&text={}".format(chat_id, msg)
        if msg is not None:
            requests.get(url) # ping telegram api to send message

    def read_token_from_env(self):
        # parser = cfg.ConfigParser()
        # parser.read(config)
        return os.environ['token']

    def get_buses(self, busStop):
        
        response = ""
        busStopName = ""

        if busStop == "KRMRT":
            busStopName = "KR-MRT"
            response += "Kent Ridge MRT\n"
        elif busStop == "UHC":
            busStopName = "STAFFCLUB"
            response += "UHC\n"
        else:
            busStopName = busStop
            response += busStopName + "\n"
        
        jsonData = json.loads(ET.fromstring(requests.get(self.getUrl(busStopName), timeout=10).text).text)

        for bus in jsonData['ShuttleServiceResult']['shuttles']:                
            if (bus['arrivalTime'] != '-'):
                response += '{} - {}\n'.format(bus['name'], bus['arrivalTime'])

        response += "\n"

        return response

    def get_rh_to_biz(self):
        yih = requests.get(self.getUrl("YIH"), timeout=10)
        museum = requests.get(self.getUrl("MUSEUM"), timeout=10)

        yih = json.loads((ET.fromstring(yih.text)).text)
        museum = json.loads((ET.fromstring(museum.text)).text)

        yih = yih['ShuttleServiceResult']['shuttles']
        yihBus = ''
        museum = museum['ShuttleServiceResult']['shuttles']
        museumBus = ''

        for bus in yih:
            arrivalTime = bus['arrivalTime']
            if (arrivalTime != '-'):
                yihBus += '{} - {}\n'.format(bus['name'], arrivalTime)

        for bus in museum:
            arrivalTime = bus['arrivalTime']
            if (bus['name'] == 'D1' or bus['name'] == 'BTC1'):
                if (bus['arrivalTime'] != '-' ):
                    museumBus += '{} - {}\n'.format(bus['name'], arrivalTime)

        return '''YIH\n{}\nMuseum\n{}\n'''.format(yihBus, museumBus)

    def get_rh_to_sci(self):
        oppYih = requests.get(self.getUrl("YIH-OPP"), timeout=10)
        museum = requests.get(self.getUrl("MUSEUM"), timeout=10)
        uhc=requests.get(self.getUrl("STAFFCLUB"), timeout=10)

        oppYih = json.loads((ET.fromstring(oppYih.text)).text)
        museum = json.loads((ET.fromstring(museum.text)).text)
        uhc = json.loads((ET.fromstring(uhc.text)).text)

        oppYih = oppYih['ShuttleServiceResult']['shuttles']
        museum = museum['ShuttleServiceResult']['shuttles']
        uhc = uhc['ShuttleServiceResult']['shuttles']

        oppYihBus = ''
        museumBus = ''
        uhcBus = ''

        for bus in oppYih:
            arrivalTime = bus['arrivalTime']
            name = bus['name']
            if (name == 'A2'):
                if (arrivalTime != '-'):
                    oppYihBus += '{} - {}\n'.format(bus['name'], arrivalTime)
        
        for bus in uhc:
            arrivalTime = bus['arrivalTime']
            if (arrivalTime != '-'):
                uhcBus += '{} - {}\n'.format(bus['name'], arrivalTime)

        for bus in museum:
            arrivalTime = bus['arrivalTime']
            name = bus['name']
            if (name == 'A2' or name == 'D2' or name == 'C'):
                if (bus['arrivalTime'] != '-' ):
                    museumBus += '{} - {}\n'.format(bus['name'], arrivalTime)

        return '''Museum\n{}\nUHC\n{}\nOPP YIH\n{}\n'''.format(museumBus, uhcBus, oppYihBus)


    def getUrl(self, busStop):
        return "https://nextbus.comfortdelgro.com.sg/testMethod.asmx/GetShuttleService?busstopname={}".format(busStop)