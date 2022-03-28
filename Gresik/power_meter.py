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
import datetime

# Load Env Key and Value
load_dotenv()
class Power_meter():
    # Inisialisasi Variabel
    def __init__(self):
            self.broker_url = os.getenv('MQTT_HOST')
            self.broker_port = int(os.getenv('MQTT_PORT'))
            self.clean_session = True
            self.topic = "gresik/powermeter"
            self.tool_status = "Online"
            self.table_name = "powermeter_gresiks"
            self.client_id = f'python-mqtt-power_meter_Gresik{random.randint(0, 1000)}'
            self.username = os.getenv('MQTT_USERNAME')
            self.password = os.getenv('MQTT_PASSWORD')
            self.connected = False
            self.Messagereceived = False
            self.voltage_indicator = 200
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
            client.subscribe([(self.topic,0)], qos=1) 
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

        topic = str(message.topic)
        date = datetime.datetime.now()
        volt_pln = message.payload.decode('utf-8').split(",")[0]
        arus_pln = message.payload.decode('utf-8').split(",")[1]
        power_pln = message.payload.decode('utf-8').split(",")[2]
        freq_pln = message.payload.decode('utf-8').split(",")[3]
        volt_genset = message.payload.decode('utf-8').split(",")[4]
        arus_genset = message.payload.decode('utf-8').split(",")[5]
        power_genset = message.payload.decode('utf-8').split(",")[6]
        freq_genset = message.payload.decode('utf-8').split(",")[7]
        full_message = message.payload.decode('utf-8')
        print(volt_pln)
        print(message.payload.decode('utf-8'))


        # # Insert to Db after receive message
        self.insertDb(topic,full_message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date)

        # # Send to telegram
        # self.send_message(volt_pln,topic,self.tool_status)


    def insertDb(self,topic,full_message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date):
        full_message = str(full_message)
        now = datetime.datetime.now()
        try:
            self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(topic,full_message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date))
        except Exception as e:
            print(e)
            print("tes")
        if(float(volt_pln) < self.voltage_indicator):
            try:
                self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(topic,full_message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date))
                self.db.commit()
            except Exception as e:
                print(e)
                print("Fail save to db")
            else:
                print("Succesfully save to database ")
    
    def send_message(self,tegangan_listrik,topic,status):
        if(float(tegangan_listrik) < self.voltage_indicator):
            try:
                telegram_send.send(messages=["Status : " + status + "\n" + "Topic On : " + topic + "\n" + "Tegangan Listrik : " + str(tegangan_listrik)])
            except Exception as e:
                print(e)
                print("There is error when sendding a message")
                self.Messagereceived = True

      




tes  = Power_meter()
tes.run()
