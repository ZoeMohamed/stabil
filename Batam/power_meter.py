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


class Powermeter():
    # Inisialisasi Variabel
    def __init__(self):
        self.broker_url = os.getenv('MQTT_HOST')
        self.broker_port = int(os.getenv('MQTT_PORT'))
        self.clean_session = True
        self.topic = "batam/powermeter"
        self.tool_status = ""
        self.table_name = "powermeter_batams"
        self.client_id = f'python-mqtt-powermeter_batams{random.randint(0, 1000)}'
        self.username = os.getenv('MQTT_USERNAME')
        self.password = os.getenv('MQTT_PASSWORD')
        self.connected = False
        self.Messagereceived = False
        self.token = os.getenv('TELEGRAM_API_TOKEN')
        self.bot = telegram.Bot(token=self.token)

        #  Volt indicator
        self.voltage_indicator = 100
        # Inisialisasi Perubahan Voltage
        self.time_trigger = 20

        self.arr_normal_voltgenset = []
        self.arr_normal_arusgenset = []
        self.arr_normal_powergenset = []
        self.arr_normal_freqgenset = []
        self.arr_normal_voltpln = []
        self.arr_normal_aruspln = []
        self.arr_normal_powerpln = []
        self.arr_normal_freqpln = []
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
            client.subscribe(self.topic, qos=1)
            client.on_message = self.on_message
            client.loop_start()

            while self.connected != True:
                time.sleep(0.1)

            while self.Messagereceived != True:

                now = datetime.datetime.now()
                sekarang = now.year * 525600 + now.month * 43800 + \
                    now.day * 1440 + now.hour * 60 + now.minute
                time_stamp = sekarang
                while True:
                    now = datetime.datetime.now()
                    sekarang = now.year * 525600 + now.month * 43800 + \
                        now.day * 1440 + now.hour * 60 + now.minute
                    print(sekarang - time_stamp)
                    time.sleep(1)

                    if self.lowest_volt is not None:
                        print("kurang dari 20 Mins")
                        print(now)
                        print(sekarang)
                        print(time_stamp)

                        self.send_message(self.lowest_volt,
                                          self.topic, self.tool_status)

                        self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                            self.arr_normal_topic[-1], self.arr_normal_message[-1], self.arr_normal_voltgenset[-1], self.arr_normal_arusgenset[-1], self.arr_normal_powergenset[-1], self.arr_normal_freqgenset[-1], self.arr_normal_voltpln[-1], self.arr_normal_aruspln[-1], self.arr_normal_powerpln[-1], self.arr_normal_freqpln[-1], datetime.date.strftime(
                                datetime.datetime.now(), "%m/%d/%Y/%H:%M:%S"), datetime.datetime.now()))
                        self.db.commit()

                        self.lowest_volt = None

                    elif(sekarang - time_stamp) >= self.time_trigger and len(self.arr_normal_voltpln) != 0:
                        print("lebih dari 20 Mins")

                        self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date,created_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                            self.arr_normal_topic[-1], self.arr_normal_message[-1], self.arr_normal_voltgenset[-1], self.arr_normal_arusgenset[-1], self.arr_normal_powergenset[-1], self.arr_normal_freqgenset[-1], self.arr_normal_voltpln[-1], self.arr_normal_aruspln[-1], self.arr_normal_powerpln[-1], self.arr_normal_freqpln[-1], datetime.date.strftime(
                                datetime.datetime.now(), "%m/%d/%Y/%H:%M:%S"), datetime.datetime.now()))
                        self.db.commit()

                        self.arr_normal_voltgenset = []
                        self.arr_normal_arusgenset = []
                        self.arr_normal_powergenset = []
                        self.arr_normal_freqgenset = []
                        self.arr_normal_voltpln = []
                        self.arr_normal_aruspln = []
                        self.arr_normal_powerpln = []
                        self.arr_normal_freqpln = []
                        self.arr_normal_message = []
                        self.arr_normal_topic = []
                        self.time_trigger = self.check_timedb()
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

    def send_message(self, tegangan_listrik, topic, status):
        print("Masuk ke send message")
        try:

            for chat_id in self.check_status():
                self.bot.sendMessage(chat_id=chat_id, text="Status : " + status + "\n" +
                                     "Topic On : " + topic + "\n" + "Tegangan Listrik : " + str(tegangan_listrik))

        except Exception as e:
            print(e)
            print("There is error when sendding a message")
            self.Messagereceived = True

    def check_status(self):

        db = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')

        )
        mydb = db.cursor()

        list_of_chatid = []
        mydb.execute('SELECT chat_id FROM ' + "user_teles " +
                     ' WHERE status=' + str(1))
        results = mydb.fetchall()
        for row in results:
            print(row)
            list_of_chatid.append("".join(row))

        print(list(set(list_of_chatid)))

        return list(set(list_of_chatid))

    def check_timedb(self):
        db = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')

        )
        mydb = db.cursor()

        mydb.execute('SELECT waktu FROM ' + "set_time_datas")
        results = mydb.fetchall()

        str = "".join(results[-1])
        print(str)

        mydb.close()
        db.close()

        return int(str)

    def on_message(self, client, userdata, message):
        topic = str(message.topic)
        date = datetime.datetime.now()
        volt_pln = float(message.payload.decode('utf-8').split(",")[0])
        arus_pln = float(message.payload.decode('utf-8').split(",")[1])
        power_pln = float(message.payload.decode('utf-8').split(",")[2])
        freq_pln = float(message.payload.decode('utf-8').split(",")[3])
        volt_genset = float(message.payload.decode('utf-8').split(",")[4])
        arus_genset = float(message.payload.decode('utf-8').split(",")[5])
        power_genset = float(message.payload.decode('utf-8').split(",")[6])
        freq_genset = float(message.payload.decode('utf-8').split(",")[7])
        convertedDict = str(message.payload.decode('utf-8'))
        print(volt_pln)
        print(message.payload.decode('utf-8'))

        current_date = datetime.datetime.now()
        formatted_date = datetime.date.strftime(
            current_date, "%m/%d/%Y/%H:%M:%S")
        print(convertedDict)

        self.comp_arr.append(volt_pln)
        self.last_volt = self.comp_arr[0]
        self.real_time_volt = self.comp_arr[-1]

        if(len(self.comp_arr) == 2):
            if(abs(self.real_time_volt - self.last_volt)) >= self.voltage_indicator:
                print("Tegangan Listrik Tidak Stabil")
                print(abs(self.last_volt - self.real_time_volt))
                self.comp_arr.pop(0)
                self.lowest_volt = self.comp_arr[-1]
                self.topics = topic
                self.full_message = convertedDict

            else:
                self.arr_normal_message.append(convertedDict)
                self.arr_normal_topic.append(topic)
                self.arr_normal_voltpln.append(volt_pln)
                self.arr_normal_voltgenset.append(volt_genset)
                self.arr_normal_aruspln.append(arus_pln)
                self.arr_normal_arusgenset.append(arus_genset)
                self.arr_normal_freqgenset.append(freq_genset)
                self.arr_normal_freqpln.append(freq_pln)
                self.arr_normal_powergenset.append(power_genset)
                self.arr_normal_powerpln.append(power_pln)

                if(len(self.arr_normal_voltpln) == 2 and len(self.arr_normal_message) == 2 and len(self.arr_normal_topic) == 2):
                    self.arr_normal_message.pop(0)
                    self.arr_normal_topic.pop(0)
                    self.arr_normal_voltpln.pop(0)
                    self.arr_normal_voltgenset.pop(0)
                    self.arr_normal_aruspln.pop(0)
                    self.arr_normal_arusgenset.pop(0)
                    self.arr_normal_freqgenset.pop(0)
                    self.arr_normal_freqpln.pop(0)
                    self.arr_normal_powergenset.pop(0)
                    self.arr_normal_powerpln.pop(0)

                print("KALO LEN NYA 2 LISTRIK DAH STABIL")

                print(self.arr_normal_message)
                print(self.arr_normal_topic)

                print("Tegangan Listrik Stabil")
                print("Sebelum di Pop")
                print(self.comp_arr)
                self.comp_arr.pop(0)
                print("Sesudah di Pop")
                print(self.comp_arr)

        elif(len(self.comp_arr) == 1):
            self.arr_normal_message.append(convertedDict)
            self.arr_normal_topic.append(topic)
            self.arr_normal_voltpln.append(volt_pln)
            self.arr_normal_voltgenset.append(volt_genset)
            self.arr_normal_aruspln.append(arus_pln)
            self.arr_normal_arusgenset.append(arus_genset)
            self.arr_normal_freqgenset.append(freq_genset)
            self.arr_normal_freqpln.append(freq_pln)
            self.arr_normal_powergenset.append(power_genset)
            self.arr_normal_powerpln.append(power_pln)


Powermeter_batam = Powermeter()
Powermeter_batam.run()
