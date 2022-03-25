from telegram.ext import Updater 
import logging 
 
from telegram import Update 
from telegram.ext import CallbackContext 
 
from telegram.ext import CommandHandler 
from telegram.ext import ChatMemberHandler 

from dotenv import load_dotenv
import os

import mysql.connector

load_dotenv()
updater = Updater( 
    token=os.getenv('TELEGRAM_API_TOKEN'), use_context=True) 
dispatcher = updater.dispatcher 
 
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
                    level=logging.INFO) 
 
dicto = {}
def start(update: Update, context: CallbackContext): 



   dicto.update({update.message.from_user.first_name:update.message.from_user.id})

   for key in dicto:
            try:
                if key in select() or key in select_other():
                    update_status(chat_id=dicto[key])
                    print("There is duplicate value when looping and insert to DB,if this prompt appears that's mean the script run sucsessfully")
                else:
                    print("sucsess")
                    insertDb(name=key,chat_id=dicto[key])
            except Exception as e:
                print(e)

def select_other():
    name_list = []
    table_name = 'user_teles'
    new = []

    try:
        db = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
       )
        mydb = db.cursor()

        mydb.execute("SELECT name FROM " + table_name)


        myresult = mydb.fetchall()

        for x in myresult:
            name_list.append(x)

        for x in name_list:
            new.append("".join(x))


    except Exception as e:
        print(e)
        print("Fail To select")


    else:
        return new

def callback_status(update: Update, context: CallbackContext): 
    status = update.my_chat_member.new_chat_member.status
    chat_id = update.my_chat_member.from_user.id
    first_name = update.my_chat_member.from_user.first_name

    print(first_name)
    print(chat_id)
    print(status)


    if (status == "kicked"):
        user_block(chat_id=chat_id)


def insertDb(name,chat_id):
    table_name = 'teleusers'

    try:
        db = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
       )
        mydb = db.cursor()
        mydb.execute(f"INSERT INTO {table_name} (name,chat_id) VALUES (%s,%s)",(name,chat_id))
        db.commit()

    except Exception as e:
        print(e)
        print("Fail save to db")

    else:
        print("Successfully save to database ")


def user_block(chat_id):
    table_name = 'teleusers'   
    table_name_2 = 'user_teles'


    try:
        db = mysql.connector.connect(
        host=os.getenv ('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
       )
        mydb = db.cursor()

        mydb.execute("DELETE FROM " + table_name + " WHERE chat_id=" + str(chat_id))
        
        mydb.execute('UPDATE ' + table_name_2 + " SET status=" + str(0) + " WHERE chat_id=" + str(chat_id) )
        mydb.execute('UPDATE ' + table_name_2 + " SET disable=" + str(1) + " WHERE chat_id=" + str(chat_id) )

        db.commit()

    except Exception as e:
        db.rollback()
        print(e)




def select():
    name_list = []
    table_name = 'teleusers'
    new = []

    try:
        db = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
       )
        mydb = db.cursor()

        mydb.execute("SELECT name FROM " + table_name)


        myresult = mydb.fetchall()

        for x in myresult:
            name_list.append(x)

        for x in name_list:
            new.append("".join(x))


    except Exception as e:
        print(e)
        print("Fail To select")


    else:
        return new


def update_status(chat_id): 
    print("TESSSS")
    table_name_2 = "user_teles"

    try:
        db = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST'),
        user=os.getenv('MYSQL_USER'),
        password=os.getenv('MYSQL_PASSWORD'),
        database=os.getenv('MYSQL_DATABASE')
       )
        mydb = db.cursor()

        mydb.execute('UPDATE ' + table_name_2 + " SET status=" + str(0) + " WHERE chat_id=" + str(chat_id) )    
        mydb.execute('UPDATE ' + table_name_2 + " SET disable=" + str(0) + " WHERE chat_id=" + str(chat_id) )    
        db.commit()


    except Exception as e:
        print(e)
        print("Fail to Update")

    
 
start_handler = CommandHandler('start', start) 
chat = ChatMemberHandler(callback=callback_status,pass_user_data=True) 
dispatcher.add_handler(chat) 
dispatcher.add_handler(start_handler)
 
updater.start_polling()

