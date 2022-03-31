

# from math import ceil
# from datetime import datetime, timedelta

# past = 20
# time_stamp = datetime.now()

# time_stamp = int(str(time_stamp).split(":")[1])
# running = True
# while running:
#     minute = int(str(datetime.now()).split(":")[1])
#     if(minute < time_stamp + 1):
#         print("Voltage track")
#         print(datetime.now())

#     else:
#         print("Run eve 20 Minutes")   
#         running = False

from datetime import datetime

now = datetime.now()
sekarang=now.hour*3600+now.minute * 60 + now.second
time_stamp = sekarang
import time
while True:
    now = datetime.now()
    sekarang=now.hour*3600+now.minute * 60 + now.second
    time.sleep(1)
    if (sekarang - time_stamp ) > 1:
        time_stamp = sekarang
        print(time_stamp)



