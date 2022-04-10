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
from datetime import date, timedelta
from math import ceil
import time


load_dotenv()
while True:
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

