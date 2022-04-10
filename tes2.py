import datetime
import time


now = datetime.datetime.now()
sekarang = now.hour*60+now.minute
time_stamp = sekarang
while True:
    now = datetime.datetime.now()
    sekarang = now.hour*60+now.minute
    print(now)
    print(sekarang)
    print(time_stamp)
    print(abs(sekarang - time_stamp))
    time.sleep(1)