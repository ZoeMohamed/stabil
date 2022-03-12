from operator import truediv
from sqlite3 import connect
import time
import paho.mqtt.client as mqttclient
import mysql.connector
import random
import json
import telebot
import telegram_send
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events
class Power_meter():
    # Inisialisasi Variabel
    def __init__(self):
            self.broker_url = '167.71.204.253'
            self.broker_port = 1883
            self.clean_session = True
            self.topic = "batam/powermeter"
            self.client_id = f'python-mqtt-{random.randint(0, 1000)}'
            self.username = 'gresik'
            self.password = 'admin.admin'
            self.connected = False
            self.Messagereceived = False
            self.token = "5206300109:AAG40KPoCBfDa9ducRB5OkCnhZX-gPqrKLU"

            # Config connect to db
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Zoemohamed22110436*",
                database="notification"

            )

            # Inisialisasi cursor untuk db
            self.mydb = self.db.cursor()

          

  
    def run(self):
        client = mqttclient.Client(client_id=self.client_id)
        client.username_pw_set(self.username, self.password)
        client.connect(self.broker_url, self.broker_port, 15)
        client.on_connect = self.on_connect
        client.subscribe(self.topic, qos=1) 
        client.on_message = self.on_message
        client.loop_start()

        while self.connected != True:
            time.sleep(0.1)

        while self.Messagereceived != True:
            time.sleep(0.1)


        client.loop_stop()


    def on_connect(self,client,userdata,flags,rc):
        if rc == 0:
            print("Client is Connected")
            self.connected = True
        else:
            print(self.broker_url)
            print("Client is not connected")


    def on_message(self,client,userdata,message):
        # Convert string to dict (data dari broker)
    
        # Ambil nilai tegangan_listrik
        tegangan_listrik = message.payload.decode('utf-8').split(".")[0]

        # Ambil nilai topic
        topic = str(message.topic)

        # Message
        print("Tegangan Listrik " + str(tegangan_listrik))
        print("Topic On " + topic)

        # Insert to Db after receive message
        # insertDb(tegangan_listrik,topic)

        # Send to telegram
        self.send_message(tegangan_listrik,topic)


    def insertDb(tegangan_listrik,topic,self):
        table_name = 'power_meter_batam'
        voltage_indicator = 213
        if(int(tegangan_listrik) < voltage_indicator):
            try:
                self.db.execute(f"INSERT INTO {table_name} (tegangan,topic) VALUES (%s,%s)",(tegangan_listrik,topic))
                self.db.commit()
            except:
                print("Fail save to db")
            else:
                print("Succesfully save to database ")
    
    def send_message(self,tegangan_listrik,topic):
        if(int(tegangan_listrik) < 215):
            telegram_send.send(messages=[str(tegangan_listrik) + topic])
      



tes  = Power_meter()
tes.run()
