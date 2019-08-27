import requests
import json
import configparser as cfg
import xml.etree.ElementTree as ET


class telegram_chatbot():
    def __init__(self, config):
        self.token = self.read_token_from_config_file(config)
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

    def read_token_from_config_file(self, config):
        parser = cfg.ConfigParser()
        parser.read(config)
        return parser.get('creds', 'token')

    def get_rh_to_biz(self):
        yih = requests.get(self.getUrl("YIH"))
        museum = requests.get(self.getUrl("MUSEUM"))

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
        
        jsonData = json.loads(ET.fromstring(requests.get(self.getUrl(busStopName)).text).text)

        for bus in jsonData['ShuttleServiceResult']['shuttles']:                
            if (bus['arrivalTime'] != '-'):
                response += '{} - {}\n'.format(bus['name'], bus['arrivalTime'])

        response += "\n"

        return response

    def getUrl(self, busStop):
        return "https://nextbus.comfortdelgro.com.sg/testMethod.asmx/GetShuttleService?busstopname={}".format(busStop)