import http.client
import urllib.parse
import time
import requests
import json
import sqlite3
def read_sound_thingspeak():
    soundURL='https://api.thingspeak.com/channels/1152850/fields/1.json?api_keys='
    soundKEY='8T5J8V8E0LX16RY5'
    soundHEADER='&results=1'
    sound_FULL=soundURL+soundKEY+soundHEADER
    soundresults=requests.get(sound_FULL).json()
    data=[]
    for x in soundresults['feeds']:
        data.append(str(x['field1']))
    print(data[0])
def read_laser_thingspeak():
    laserKEY='QEAI32EFVL4ZM7ZR'
    laserURL= 'https://api.thingspeak.com/channels/1150122/fields/1.json?api_key='
    laserHEADER ='&results=1'
    laser_FULL = laserURL+laserKEY+laserHEADER
    laserresults=requests.get(laser_FULL).json()
    data2=[]
    for x in laserresults['feeds']:
        data2.append(str(x['field1']))
    print(data2[0])
    
def read_motion_thingspeak():    
    motionURL='https://api.thingspeak.com/channels/1219425/fields/1.json?api_key='
    motionKEY='GQ6EDK3P60AS7YLO'
    motionHEADER='&results=1'
    motion_FULL=motionURL+motionKEY+motionHEADER
    motionresults=requests.get(motion_FULL).json()
    data3=[]
    for x in motionresults['feeds']:
        data3.append(str(x['field1']))
    print(data3[0])
    
if __name__ == '__main__':
    
    read_sound_thingspeak()
    read_laser_thingspeak()
    read_motion_thingspeak()
    
