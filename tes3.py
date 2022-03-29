from datetime import datetime,timedelta

now = datetime.now()
mydate = datetime(2012,9,28,10,55)
mystart = now.replace(hour=10, minute=55, second=0)
myend = datetime.now() + timedelta(minutes=2)

print(myend)
if mystart <= mydate < myend:
    print("dumb")