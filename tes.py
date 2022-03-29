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
            client.subscribe([(self.topic,0),(self.status,0)], qos=1)
            client.on_message = self.on_message
            client.loop_start()

            while self.connected != True:
                time.sleep(0.1)

            while self.Messagereceived != True:
                time.sleep(0.1)


            client.loop_stop()
        except Exception as e:
            print(e)



    def on_connect(self,client,userdata,flags,rc):
        if rc == 0:
            print("Client is Connected")
            self.connected = True
        else:
            print("Client is not connected")



    def on_message(self,client,userdata,message):


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
            formatted_date = datetime.date.strftime(current_date, "%m/%d/%Y/%H:%M:%S")

            # print(convertedDict)

            # print(formatted_date)


            

            # # Insert to Db after receive message
            self.insertDb(topic,convertedDict,tegangan_listrik,formatted_date,current_date)

       

    def every_spec_minutes():
        pass

    def insertDb(self,topic,full_message,tegangan_listrik,formatted_date,current_date):
        full_message = str(full_message)
        print(full_message)



        listo = []

        
        try:

            if tegangan_listrik < 210 :
                self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt,date,created_at) VALUES (%s,%s,%s,%s,%s)",(topic,full_message,tegangan_listrik,formatted_date,current_date))
                self.db.commit()

            elif tegangan_listrik :
                pass

           
        except Exception as e:
            print(e)
            self.Messagereceived = True
            print("Fail save to db")
        else:
            print("Succesfully save to database ")





Server_gresik = Server()
Server_gresik.run()

