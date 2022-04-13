from pydoc import importfile


import datetime

import time


now = datetime.datetime.now()
sekarang = now.year*10000 + 100 * now.month  + now.day + now.hour*60+now.minute
time_stamp = sekarang


while True:
    now = datetime.datetime.now()
    sekarang = now.year*10000 + 100 * now.month  + now.day + now.hour*60+now.minute
    print(abs(sekarang - time_stamp))
    print(now.hour * 60 + now.minute)
    print(now)
    print(sekarang)
    time.sleep(1)

    if (abs(sekarang - time_stamp) >= 1445):
        print("GG BANG")
        time_stamp = sekarang
