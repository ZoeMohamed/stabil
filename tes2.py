

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
import time


# now = datetime.now()
# sekarang = now.hour*3600+now.minute*60
# time_stamp = sekarang
# while True:
#     now = datetime.now()
#     sekarang = now.hour*3600+now.minute*60
#     print(sekarang)
#     time.sleep(1)
#     print(sekarang)
# c

now = datetime.now()
print(now.hour * 60 + now.minute)
