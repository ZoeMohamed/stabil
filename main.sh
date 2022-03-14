#!/bin/bash 
python3 /home/zoe/python-notification/Batam/ais.py &  
python3 /home/zoe/python-notification/Batam/ac_growatt.py &
python3 /home/zoe/python-notification/Batam/cctv.py &
python3 /home/zoe/python-notification/Batam/server.py &
python3 /home/zoe/python-notification/Batam/ac_aki.py &
python3 /home/zoe/python-notification/Batam/charger_aki_ac.py &
python3 /home/zoe/python-notification/Batam/power_meter.py &


python3 /home/zoe/python-notification/Gresik/ac_aki.py &
python3 /home/zoe/python-notification/Gresik/ac_growatt.py &
python3 /home/zoe/python-notification/Gresik/ais.py &
python3 /home/zoe/python-notification/Gresik/cctv.py &
python3 /home/zoe/python-notification/Gresik/mikrotik.py &
python3 /home/zoe/python-notification/Gresik/server.py &
python3 /home/zoe/python-notification/Gresik/power_meter.py 


