# from pydoc import importfile


# import datetime

# import time


# now = datetime.datetime.now()
# sekarang = now.year*10000 + 100 * now.month  + now.day + now.hour*60+now.minute
# time_stamp = sekarang


# while True:
#     now = datetime.datetime.now()
#     sekarang = now.year*10000 + 100 * now.month  + now.day + now.hour*60+now.minute
#     print(sekarang - time_stamp)
#     time.sleep(1)

#     if (sekarang - time_stamp >= 1):
#         print("woi")


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


        self.mydb.execute(f"INSERT INTO {self.table_name} (topic,message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(topic,full_message,volt_genset,arus_genset,power_genset,freq_genset,volt_pln,arus_pln,power_pln,freq_pln,date))
                self.db.commit()