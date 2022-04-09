
from importlib import import_module
from dotenv import load_dotenv
import paho.mqtt.client as mqttclient
import mysql.connector

import time
import os
import datetime


import random

# Load Env Key and Value
load_dotenv()
class Power_meter():
    # Inisialisasi Variabel
    def __init__(self):
          
            self.topic = "gresik/powermeter"
            self.tool_status = "Online"
            self.table_name = "powermeter_gresiks"
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
            


          



    def on_message(self):
        dict = {212.35:41.51,203.75:40.55,201.75:44.20,210.25:42.59,202.15:41.30,217.15:41.22,211.11:50.50,210.49:45.10,209.90:42.21,201.15:41.75}
        for k,v in dict.items() :
            dummy_message = f"{k},3.844,543.60,2.714,{v},0.66,0.00,0.000,0.00,0.000,0.00,0.00,572,37.56,-1,1"
            topic = "batam/powermeter"
            current_date = datetime.datetime.now()
            formatted_date = datetime.date.strftime(current_date, "%m/%d/%Y/%H:%M:%S")  
            volt_pln = dummy_message.split(",")[0]
            arus_pln = dummy_message.split(",")[1]
            power_pln = dummy_message.split(",")[2]
            freq_pln = dummy_message.split(",")[3]
            volt_genset = dummy_message.split(",")[4]
            arus_genset = dummy_message.split(",")[5]
            power_genset = dummy_message.split(",")[6]
            freq_genset = dummy_message.split(",")[7]
            full_dummy_message = dummy_message

            print(dummy_message)
            print(topic)
            print(arus_pln)
            print(power_pln)



            # # Insert to Db after receive message
            self.insertDb(topic,full_dummy_message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,formatted_date,current_date)

            # # Send to telegram
            # self.send_message(volt_pln,topic,self.tool_status)

            time.sleep(120)


    def insertDb(self,topic,full_message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,formatted_date,current_date):
        full_message = str(full_message)
        now = datetime.datetime.now()
    
        try:
            self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(topic,full_message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,formatted_date,current_date))
            self.db.commit()
        except Exception as e:
            print(e)
            print("Fail save to db")
        else:
            print("Succesfully save to database ")


      




tes  = Power_meter()
tes.on_message()
