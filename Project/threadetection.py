import schedule
import time
from threading import Thread
import http.client
import urllib.parse
import time
import requests
import json
import sqlite3
import datetime
from dateutil import parser
import pytz

ONE_MINUTE=60

class threatdetect:

    def __init__(self):
        self.sounddetected=0
        self.soundtime=0
        self.laserdetected=0
        self.lasertime=0
        self.motiondetected=0
        self.motiontime=0

    def determinethreat(self): #This method is the multithreading to run the methods all together
        f=threatdetect()
        soundthingspeak = Thread(target=f.read_sound_thingspeak)
        soundthingspeak.start()
        soundthingspeak.join()
        laserthingspeak = Thread(target=f.read_laser_thingspeak)
        laserthingspeak.start()
        laserthingspeak.join()
        motionthingspeak = Thread(target=f.read_motion_thingspeak)
        motionthingspeak.start()
        motionthingspeak.join()
        fullthreatlevel = Thread(target=f.threatlevel)
        fullthreatlevel.start()
        fullthreatlevel.join()
    
    def threatlevel(self):
        '''global self.sounddetected 
        global soundtime 
        global laserdetected 
        global lasertime 
        global motiondetected 
        global motiontime'''
        '''The below code goes through all the possibilities for threat levels for sensors, it will compare the time that the sensor was tripped to the
            current time to determine if the sensor was recently tripped or if it just grabbed an old reading'''
    
        if self.laserdetected ==1 and self.sounddetected ==1 and self.motiondetected ==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <ONE_MINUTE:
                print("Threat level 3, all sensors have been tripped")
       
    
        elif self.laserdetected == 1 and self.sounddetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <ONE_MINUTE:
                print("Threat level 2,laser has been broken and soundhas been detected too please listen to most recent audio file")
       
        elif self.motiondetected == 1 and self.sounddetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <ONE_MINUTE:
                print("Threat level 2, motion has been detected and so has sound please listen to most recent audio file")
          
        elif self.motiondetected == 1 and self.laserdetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE:
                print("Threat level 2, motion has been detected and laser has been tripped")
          
        elif self.sounddetected==1 and(datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds()<ONE_MINUTE:
                print("Threat level 1, sound has been detected please listen to most recent audio file")
           
            
        elif self.laserdetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE:
                print("Threat level 1, tripwire has been broken")
          
            
        elif self.motiondetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE:
                print("Threat level 1, motion has been detected")
            
        else:
            print("you safe homie")
        
    
    def read_sound_thingspeak(self):
        '''The following code reads if the sound sensor has been triggered and stores that time in an array, it also stores the time
            it happened at in another array'''
        #global sounddetected
        #global soundtime
        soundURL='https://api.thingspeak.com/channels/1152850/fields/1.json?api_keys='
        soundKEY='8T5J8V8E0LX16RY5'
        soundHEADER='&results=1' 
        sound_FULL=soundURL+soundKEY+soundHEADER
        soundresults=requests.get(sound_FULL).json()
        soundURL2='https://api.thingspeak.com/channels/1152850/fields/2.json?api_keys='
        soundKEY2='8T5J8V8E0LX16RY5'
        soundHEADER2='&results=1' 
        sound_FULL2=soundURL2+soundKEY2+soundHEADER2
        soundresults2=requests.get(sound_FULL2).json()
        data=[]
        for x in soundresults['feeds']:
            data.insert(0,int(x['field1']))
            self.sounddetected = data[0]
        for x in soundresults2['feeds']:
            data.insert(1,str(x['created_at']))
            self.soundtime=data[1]
        
        
    
    
    def read_laser_thingspeak(self):
        '''The following code reads if the laser tripwire sensor has been triggered and stores that time in an array, it also stores the time
        it happened at in another array'''
        #global self.laserdetected
        laserKEY='QEAI32EFVL4ZM7ZR'
        laserURL= 'https://api.thingspeak.com/channels/1150122/fields/1.json?api_key='
        laserHEADER ='&results=1'
        laser_FULL = laserURL+laserKEY+laserHEADER
        laserresults=requests.get(laser_FULL).json()
        data2=[]
        for x in laserresults['feeds']:
            data2.insert(0,int(x['field1']))
            self.laserdetected = data2[0]
        for x in laserresults['feeds']:
            data2.insert(1,str(x['created_at']))
            self.lasertime=data2[1]
        
    
    def read_motion_thingspeak(self):
        '''The following code reads if the motion sensor has been triggered and stores that time in an array, it also stores the time
        it happened at in another array'''
        #global motiondetected
        #global motiontime
        motionURL='https://api.thingspeak.com/channels/1219425/fields/1.json?api_key='
        motionKEY='GQ6EDK3PONE_MINUTEAS7YLO'
        motionHEADER='&results=1'
        motion_FULL=motionURL+motionKEY+motionHEADER
        motionresults=requests.get(motion_FULL).json()
        data3=[]
        print(motionresults)
        for x in motionresults['feeds']:
            data3.insert(0,int(x['field1']))
            self.motiondetected=data3[0]
        for x in motionresults['feeds']:
            data3.insert(1,str(x['created_at']))
            self.motiontime=data3[1]
            
#This will run the multithreading every 5 seconds to always be checking for activity
ah=threatdetect()
schedule.every(5).seconds.do(ah.determinethreat)



while True:
    schedule.run_pending()
    time.sleep(1)
