from math import ceil
from datetime import datetime, timedelta
import time

from math import ceil
from datetime import datetime, timedelta

i = 0
is_printed = False


def to_second(minute):
    return minute * 60


while True:
    ts = datetime.now()
    ts = ts.replace(second=0, microsecond=0) + \
        timedelta(seconds=ceil(ts.second/to_second(2))*to_second(2))

    xs = datetime.now()
    xs = xs.replace(second=0, microsecond=0)

    if(xs.minute == ts.minute):
        time.sleep(1)
        print(xs)
        print(ts)
