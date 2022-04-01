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
        self.topic = "tele/batam/ais/SENSOR"
        self.status = "tele/batam/ais/LWT"
        self.tool_status = ""
        self.table_name = "aisfuruno_batams"
        self.client_id = f'python-mqtt-server_gresiks{random.randint(0, 1000)}'
        self.username = os.getenv('MQTT_USERNAME')
        self.password = os.getenv('MQTT_PASSWORD')
        self.connected = False
        self.Messagereceived = False
        self.voltage_indicator = 209
        self.token = os.getenv('TELEGRAM_API_TOKEN')
        self.bot = telegram.Bot(token=self.token)
        self.low_volt = None
        self.time_trigger = 10
        self.low_message = None
        self.low_topic = None
        self.arr_normal_volt = []
        self.arr_normal_message = []
        self.arr_normal_topic = []
        self.volt_trigger = 200


        # Inisialisasi Perubahan Voltage
        self.comp_arr = []
        self.last_volt = None
        self.real_time_volt = None
        self.lowest_volt = None

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
                sekarang = now.hour*3600+now.minute
                time_stamp = sekarang
                while True:
                    now = datetime.datetime.now()
                    sekarang = now.hour*3600+now.minute
                    print(sekarang - time_stamp)
                    time.sleep(1)

                    

                    if self.lowest_volt is not None:
                        print("kurang dari 20 Mins")
                        print(now)
                        print(sekarang)
                        print(time_stamp)
                        current_date = datetime.datetime.now()
                        formatted_date = datetime.date.strftime(
                            current_date, "%m/%d/%Y/%H:%M:%S")
                        self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt,date,created_at) VALUES (%s,%s,%s,%s,%s)", (
                            "tes", str("tes data "), self.lowest_volt, formatted_date, current_date))
                        self.db.commit()
                        self.lowest_volt = None

                    elif(sekarang - time_stamp) >= self.time_trigger and len(self.arr_normal_topic) != 0 and len(self.arr_normal_message) != 0 and len(self.arr_normal_volt) != 0:
                        print("lebih dari 20 Mins")
                        print(now)
                        print(sekarang)
                        print(time_stamp)
                        current_date = datetime.datetime.now()
                        formatted_date = datetime.date.strftime(
                            current_date, "%m/%d/%Y/%H:%M:%S")
                        self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt,date,created_at) VALUES (%s,%s,%s,%s,%s)", (
                            self.arr_normal_topic[-1], str(self.arr_normal_message[-1]), self.arr_normal_volt[-1], formatted_date, current_date))
                        self.db.commit()
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
            self.low_volt = tegangan_listrik

        
            self.comp_arr.append(tegangan_listrik)


            # Inisialisasi
            self.last_volt = self.comp_arr[0]
            self.real_time_volt = self.comp_arr[-1]
            if(len(self.comp_arr) == 2):
                if(abs(self.real_time_volt - self.last_volt)) >3:
                    print("tegangan gak Normal")
                    print(abs(self.last_volt - self.real_time_volt))
                    self.comp_arr.remove(self.real_time_volt if (self.real_time_volt < self.last_volt)  else self.last_volt)
                    self.lowest_volt = self.comp_arr[-1]
                    print(self.real_time_volt)

                else:
                    # Delete the latest voltage 
                    print("Sebelum di Pop")
                    print(self.comp_arr)
                    self.comp_arr.pop(0)
                    print("Sesudah di Pop")
                    print(self.comp_arr)
                 
            if(tegangan_listrik >215):
                self.arr_normal_volt.append(tegangan_listrik)
                self.arr_normal_message.append(convertedDict)
                self.arr_normal_topic.append(topic)


Server_gresik = Server()
Server_gresik.run()
