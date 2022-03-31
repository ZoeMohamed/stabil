from queue import Empty
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
        self.volt = None

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
    # def insert_volt(self):



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

                now = datetime.datetime.now()
                sekarang=now.hour*3600+now.minute
                time_stamp = sekarang
                while True:
                    now = datetime.datetime.now()
                    sekarang=now.hour*3600+now.minute
                    time.sleep(1)

                    if (sekarang - time_stamp ) < 1 and self.volt is not None:
                        current_date = datetime.datetime.now()
                        formatted_date = datetime.date.strftime(current_date, "%m/%d/%Y/%H:%M:%S")
                        self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt,date,created_at) VALUES (%s,%s,%s,%s,%s)",("tes","tes",self.volt,formatted_date,current_date))
                        self.db.commit()
                        time_stamp = sekarang

                    elif(sekarang - time_stamp) >= 1:
                        print("mantap")
                        time_stamp = sekarang
                        





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


            print(convertedDict)

            if(tegangan_listrik < 210):
                self.volt = tegangan_listrik    

Server_gresik = Server()
Server_gresik.run()



