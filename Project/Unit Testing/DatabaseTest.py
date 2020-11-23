import http.client
import urllib.parse
import time
import sqlite3
import requests
import json
sound=""
laser=""
motion=""


def read_sound_thingspeak():
    global sound
    data=[]
    soundURL='https://api.thingspeak.com/channels/1152850/fields/1.json?api_keys='
    soundKEY='8T5J8V8E0LX16RY5'
    soundHEADER='&results=1'
    sound_FULL=soundURL+soundKEY+soundHEADER
    soundresults=requests.get(sound_FULL).json()
    
    for x in soundresults['feeds']:
        data.append(str(x['field1']))
    print(data[0])
    sound=data[0]
def read_laser_thingspeak():
    global laser
    data2=[]
    laserKEY='QEAI32EFVL4ZM7ZR'
    laserURL= 'https://api.thingspeak.com/channels/1150122/fields/1.json?api_key='
    laserHEADER ='&results=1'
    laser_FULL = laserURL+laserKEY+laserHEADER
    laserresults=requests.get(laser_FULL).json()
    
    for x in laserresults['feeds']:
        data2.append(str(x['field1']))
    print(data2[0])
    laser=data2[0]
def read_motion_thingspeak():
    global motion
    data3=[]
    motionURL='https://api.thingspeak.com/channels/1219425/fields/1.json?api_key='
    motionKEY='GQ6EDK3P60AS7YLO'
    motionHEADER='&results=1'
    motion_FULL=motionURL+motionKEY+motionHEADER
    motionresults=requests.get(motion_FULL).json()
   
    for x in motionresults['feeds']:
        data3.append(str(x['field1']))
    print(data3[0])
    motion=data3[0]
def create():
    try:
        c.execute("""CREATE TABLE sound
                 (start, end, score)""")
    except:
        pass

def insert():
    c.execute("""INSERT INTO sound VALUES(?,?,?)""",
              (sound, laser, motion))

def select(verbose=True):
    sql = "SELECT * FROM sound"
    recs = c.execute(sql)
    if verbose:
        for row in recs:
            print (row)

db_path = '/home/pi/Desktop/Sysc3010/Project/soundsensor.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()
read_sound_thingspeak()
read_laser_thingspeak()
read_motion_thingspeak()
create()
insert()
conn.commit() #commit needed
c.execute('PRAGMA integrity_check;')
select()
c.close()
