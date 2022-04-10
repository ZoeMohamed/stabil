 
import mysql.connector
from dotenv import load_dotenv, set_key
import os

load_dotenv()

def check_timedb():
        db = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST'),
            user=os.getenv('MYSQL_USER'),
            password=os.getenv('MYSQL_PASSWORD'),
            database=os.getenv('MYSQL_DATABASE')

        )
        mydb = db.cursor()

        list_of_chatid = []
        mydb.execute('SELECT waktu FROM ' + "set_time_datas")
        results = mydb.fetchall()
        for row in results:
            print(row)
            list_of_chatid.append("".join(row))

        print(list(set(list_of_chatid)))

        return list(set(list_of_chatid))


check_timedb()