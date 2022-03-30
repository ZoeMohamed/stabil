import time
from dotenv import load_dotenv
import paho.mqtt.client as mqttclient
import mysql.connector
import random
import json
import os
import datetime
import telegram
from math import ceil
from datetime import timedelta
from math import ceil
import time

# Load Env Key and Value
load_dotenv()


class Server():
    # Inisialisasi Variabel
    def __init__(self):
        self.broker_url = os.getenv('MQTT_HOST')
        self.broker_port = int(os.getenv('MQTT_PORT'))
        self.clean_session = True
        self.topic = "tele/gresik/server/SENSOR"
        self.status = "tele/gresik/server/LWT"
        self.tool_status = ""
        self.table_name = "server_gresiks"
        self.client_id = f'python-mqtt-server_gresiks{random.randint(0, 1000)}'
        self.username = os.getenv('MQTT_USERNAME')
        self.password = os.getenv('MQTT_PASSWORD')
        self.connected = False
        self.Messagereceived = False
        self.voltage_indicator = 209
        self.token = os.getenv('TELEGRAM_API_TOKEN')
        self.bot = telegram.Bot(token=self.token)

        try:
            self.db = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE')

            )
            self.mydb = self.db.cursor()
        except:
            self.Messagereceived = True
            print("Error when connecting to Database")
            print("The Loop Stop")
        else:
            self.db = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE')

            )
            self.mydb = self.db.cursor()

    def run(self):
        try:
            client = mqttclient.Client(client_id=self.client_id)
            client.username_pw_set(self.username, self.password)
            client.connect(self.broker_url, self.broker_port, 15)
            client.on_connect = self.on_connect
            client.subscribe([(self.topic, 0), (self.status, 0)], qos=1)
            client.on_message = self.on_message
            client.loop_start()

            while self.connected != True:
                time.sleep(0.1)

            while self.Messagereceived != True:
                time_stamp = datetime.datetime.now()
                time_stamp = int(str(time_stamp).split(":")[1])
                running = True
                while running:
                    minute = int(str(datetime.datetime.now()).split(":")[1])
                    if(minute < time_stamp + 1):
                        # do something
                        pass
                    else:
                        print("Run function every 20 Mins")
                        running = False
                time.sleep(0.1)

            client.loop_stop()
        except Exception as e:
            print(e)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Client is Connected")
            self.connected = True
        else:
            print("Client is not connected")

    def on_message(self, client, userdata, message):

        if(message.payload.decode('utf-8') == "Online" or message.payload.decode('utf-8') == "Offline"):
            print("Status : " + message.payload.decode('utf-8'))
            self.tool_status = message.payload.decode('utf-8')
        else:

            # # Ambil nilai topic
            topic = str(message.topic)

            # # Convert string to dict (data dari broker)
            convertedDict = json.loads(message.payload.decode('utf-8'))

            # # Ambil nilai tegangan_listrik
            tegangan_listrik = int(convertedDict['ENERGY']['Voltage'])

            current_date = datetime.datetime.now()
            formatted_date = datetime.date.strftime(
                current_date, "%m/%d/%Y/%H:%M:%S")

            # print(convertedDict)

            # print(formatted_date)

            # # Insert to Db after receive message
            self.insertDb(topic, convertedDict, tegangan_listrik,
                          formatted_date, current_date)

    def to_second(self, minute):
        return minute * 60

    def insertDb(self, topic, full_message, tegangan_listrik, formatted_date, current_date):
        full_message = str(full_message)
        print(full_message)


Server_gresik = Server()
Server_gresik.run()


def loop_b():
    while True:
        ts = datetime.datetime.now()
        ts = ts.replace(second=0, microsecond=0) + \
            timedelta(seconds=ceil(ts.second/60)*60)

        xs = datetime.datetime.now()
        xs = xs.replace(second=0, microsecond=0)

        if(xs.minute == ts.minute):
            time.sleep(1)
            print(xs)
            print(ts)
