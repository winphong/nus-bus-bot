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

    def get_closest(self):
        yih = requests.get("https://nextbus.comfortdelgro.com.sg/testMethod.asmx/GetShuttleService?busstopname=YIH")
        museum = requests.get("https://nextbus.comfortdelgro.com.sg/testMethod.asmx/GetShuttleService?busstopname=MUSEUM")

        yih = json.loads((ET.fromstring(yih.text)).text)
        museum = json.loads((ET.fromstring(museum.text)).text)

        yih = yih['ShuttleServiceResult']['shuttles']
        yihBus = ''
        museum = museum['ShuttleServiceResult']['shuttles']
        museumBus = ''

        # closestBusStop = ''
        
        try:
            minArrivalTime = int(yih[0]['arrivalTime']) 
        except:
            if (yih[0]['arrivalTime'] == 'Arr'):
                minArrivalTime = 0
            else:
                minArrivalTime = '-'

        for bus in yih:
            
            if ( minArrivalTime != '-' and bus['arrivalTime'] != '-' ):

                if (bus['arrivalTime'] == 'Arr'):
                    arrivalTime = 0
                else:
                    arrivalTime = int(bus['arrivalTime'])

                if (arrivalTime <= minArrivalTime):
                    minArrivalTime = arrivalTime
                    # closestBusStop += '{} - {}\n'.format(
                    #     bus['name'], bus['arrivalTime']
                    # )
                
                yihBus += '{} - {}\n'.format(bus['name'], arrivalTime)

        for bus in museum:

            if (bus['name'] == 'D1' or bus['name'] == 'BTC1'):
                if ( minArrivalTime != '-' and bus['arrivalTime'] != '-' ):

                    if (bus['arrivalTime'] == 'Arr'):
                        arrivalTime = 0
                    else:
                        arrivalTime = int(bus['arrivalTime'])

                    if (arrivalTime < minArrivalTime):
                        minArrivalTime = arrivalTime
                        # closestBusStop += '{} - {}\n'.format(
                        #     bus['name'], bus['arrivalTime']
                        # )

                    museumBus += '{} - {}\n'.format(bus['name'], arrivalTime)

        return '''YIH\n{}\nMuseum\n{}\n'''.format(yihBus, museumBus)