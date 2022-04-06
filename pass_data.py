import time
from dotenv import load_dotenv, set_key
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


class Ac_aki():
    # Inisialisasi Variabel
    def __init__(self):
        self.broker_url = os.getenv('MQTT_HOST')
        self.broker_port = int(os.getenv('MQTT_PORT'))
        self.clean_session = True
        self.topic = "tele/batam/ac_aki/SENSOR"
        self.status = "tes2"
        self.tool_status = ""
        self.table_name = "acaki_batams"
        self.client_id = f'python-mqtt-ac_growatt_gresiks{random.randint(0, 1000)}'
        self.username = os.getenv('MQTT_USERNAME')
        self.password = os.getenv('MQTT_PASSWORD')
        self.connected = False
        self.Messagereceived = False
        self.token = os.getenv('TELEGRAM_API_TOKEN')
        self.bot = telegram.Bot(token=self.token)


        # Inisialisasi Perubahan Voltage
        self.time_trigger = 20
        self.arr_normal_volt = []
        self.arr_normal_message = []
        self.arr_normal_topic = []
        self.comp_arr = []
        self.last_volt = None
        self.real_time_volt = None
        self.lowest_volt = None
        self.topics = None
        self.full_message = None

        try:
            self.db = mysql.connector.connect(
                host=os.getenv('MYSQL_HOST'),
                user=os.getenv('MYSQL_USER'),
                password=os.getenv('MYSQL_PASSWORD'),
                database=os.getenv('MYSQL_DATABASE')

            )
            self.mydb = self.db.cursor()
        except Exception as e:
            print(e)
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
            client.subscribe(self.status)
            client.on_message = self.on_message
            client.loop_start()

            while self.connected != True:
                time.sleep(0.1)

            while self.Messagereceived != True:
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


    def send_message(self,tegangan_listrik,topic,status):
            print("Masuk ke send message")
            try:

                for chat_id in self.check_status():
                    self.bot.sendMessage(chat_id=chat_id, text="Status : " + status + "\n" + "Topic On : " + topic + "\n" + "Tegangan Listrik : " + str(tegangan_listrik))      


            except Exception as e:
                print(e)
                print("There is error when sendding a message")
                self.Messagereceived = True

    





    def on_message(self, client, userdata, message):

       print(message)

            


Acaki_batam = Ac_aki()
Acaki_batam.run()
