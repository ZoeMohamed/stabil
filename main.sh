#!/bin/bash 
python3.7 ${PWD}/Batam/ais.py &  
python3.7 ${PWD}/Batam/ac_growatt.py &
python3.7 ${PWD}/Batam/cctv.py &
python3.7 ${PWD}/Batam/server.py &
python3.7 ${PWD}/Batam/charger_aki_ac.py &
python3.7 ${PWD}/apiHelper/handler.py &
python3.7 ${PWD}/Gresik/ac_growatt.py &
python3.7 ${PWD}/Gresik/ais.py &
python3.7 ${PWD}/Gresik/cctv.py &
python3.7 ${PWD}/Gresik/mikrotik.py &
python3.7 ${PWD}/Gresik/server.py &
python3.7 ${PWD}/Gresik/ac_aki.py &
python3.7 ${PWD}/Batam/solar_level.py 
python3.7 ${PWD}/Batam/power_meter.py 



