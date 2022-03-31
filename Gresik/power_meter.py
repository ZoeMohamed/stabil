import time
from dotenv import load_dotenv
import paho.mqtt.client as mqttclient
import mysql.connector
import random
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




    def send_message(self,tegangan_listrik,topic,status):
        if(int(tegangan_listrik) < self.voltage_indicator):
            try:

                for chat_id in self.check_status():
                    self.bot.sendMessage(chat_id=chat_id, text="Status : " + status + "\n" + "Topic On : " + topic + "\n" + "Tegangan Listrik : " + str(tegangan_listrik))      


            except Exception as e:
                print(e)
                print("There is error when sendding a message")
                self.Messagereceived = True

    

    def check_status(self):

            db= mysql.connector.connect(
                        host=os.getenv('MYSQL_HOST'),
                        user=os.getenv('MYSQL_USER'),
                        password=os.getenv('MYSQL_PASSWORD'),
                        database=os.getenv('MYSQL_DATABASE')

                    )
            mydb = db.cursor()

            list_of_chatid = []
            mydb.execute('SELECT chat_id FROM ' + "user_teles " + ' WHERE status=' + str(1))
            results = mydb.fetchall()
            for row in results:
                print(row)
                list_of_chatid.append("".join(row))
            
            print(list(set(list_of_chatid)))

            return list(set(list_of_chatid))


      



Power_meter_gresik  = Power_meter()
Power_meter_gresik.run()
