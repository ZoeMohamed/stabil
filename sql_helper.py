# from operator import truediv
# from sqlite3 import connect
# import time
# import paho.mqtt.client as mqttclient
# import mysql.connector
# from os import listdir
# from os.path import isfile, join


# mypath = "/home/zoe/python-notification/Batam"

# onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath,f))]
# parse_files = [f.split(".")[0] + "_batam" for f in onlyfiles]

# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Zoemohamed22110436*",
#     database="notification"

# )

# mycursor = db.cursor()


# for x in parse_files:
#     mycursor.execute(f"ALTER TABLE {x} add column created_at timestamp not null default current_timestamp")

#     # mycursor.execute(f"CREATE TABLE {x} (id int primary key auto_increment, tegangan int not null,topic varchar(255) not null)")


