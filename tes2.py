

from math import ceil
from datetime import datetime, timedelta

past = 20
time_stamp = datetime.now()

time_stamp = int(str(time_stamp).split(":")[1])
running = True
while running:
    minute = int(str(datetime.now()).split(":")[1])
    if(minute < time_stamp + 1):
        print("belum kelar")
        print(datetime.now())

    else:
        print("udah kelar")   
        running = False