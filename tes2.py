from datetime import date
from datetime import datetime
today = date.today()
midnight = datetime.combine(today, datetime.min.time())
 
print('Midnight: %s ' % (midnight) )



now = datetime.now()
sekarang = now.year*10000 + 100 * now.month  + now.day + now.hour*60+now.minute

print(sekarang)