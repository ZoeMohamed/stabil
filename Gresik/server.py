from operator import truediv
from sqlite3 import connect
import time
from dotenv import load_dotenv
import paho.mqtt.client as mqttclient
import mysql.connector
import random
import json
from simplejson import load
import telebot
import telegram_send
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
import os

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
            self.table_name = "server_Gresik"
            self.client_id = f'python-mqtt-server_gresik{random.randint(0, 1000)}'
            self.username = os.getenv('MQTT_USERNAME')
            self.password = os.getenv('MQTT_PASSWORD')
            self.connected = False
            self.Messagereceived = False
            self.voltage_indicator = 250
            self.token = os.getenv('TELEGRAM_API_TOKEN')

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
            # # Convert string to dict (data dari broker)
            convertedDict = json.loads(message.payload.decode('utf-8'))
        
            # # Ambil nilai tegangan_listrik
            tegangan_listrik = int(convertedDict['ENERGY']['Voltage'])
            power = int(convertedDict['ENERGY']['Power'])


            # # Ambil nilai topic
            topic = str(message.topic)

            # # Message
            # print("Message Received " + str(convertedDict))
            # print("Tegangan Listrik " + str(tegangan_listrik))
            print("Topic On " + topic)

            # # Insert to Db after receive message
            self.insertDb(topic,tegangan_listrik,power,convertedDict)

            # # Send to telegram
            self.send_message(tegangan_listrik,topic,self.tool_status)


    def insertDb(self,topic,tegangan_listrik,power,full_message):
        full_message = str(full_message)
        print(full_message)
        try:
            self.mydb.execute(f"INSERT INTO {self.table_name} (Topic,Voltage,Power,Full_message) VALUES (%s,%s,%s,%s)",(topic,tegangan_listrik,power,full_message))
        except Exception as e:
            print(e)
            print("tes")
        if(int(tegangan_listrik) < self.voltage_indicator):
            try:
                self.mydb.execute(f"INSERT INTO {self.table_name} (Topic,Voltage,Power,Full_message) VALUES (%s,%s,%s,%s)",(topic,tegangan_listrik,power,full_message))
                self.db.commit()
            except Exception as e:
                print(e)
                print("Fail save to db")
            else:
                print("Succesfully save to database ")
    
    def send_message(self,tegangan_listrik,topic,status):
        if(int(tegangan_listrik) < self.voltage_indicator):
            try:
                telegram_send.send(messages=["Status : " + status + "\n" + "Topic On : " + topic + "\n" + "Tegangan Listrik : " + str(tegangan_listrik)])
            except Exception as e:
                print(e)
                print("There is error when sendding a message")
                self.Messagereceived = True

      




tes  = Server()
tes.run()
