#!/bin/bash 
python3.8 ${PWD}/apiHelper/handler.py &
python3.8 ${PWD}/Batam/ais.py &  
python3.8 ${PWD}/Batam/ac_growatt.py &
python3.8 ${PWD}/Batam/cctv.py &
python3.8 ${PWD}/Batam/server.py &
python3.8 ${PWD}/Batam/charger_aki_ac.py &
python3.8 ${PWD}/Batam/solar_level.py &
python3.8 ${PWD}/Batam/power_meter.py &



python3.8 ${PWD}/Gresik/ais.py &  
python3.8 ${PWD}/Gresik/ac_growatt.py &
python3.8 ${PWD}/Gresik/cctv.py &
python3.8 ${PWD}/Gresik/server.py &
python3.8 ${PWD}/Gresik/mikrotik.py &
python3.8 ${PWD}/Gresik/ac_aki.py &
python3.8 ${PWD}/Gresik/power_meter.py &







