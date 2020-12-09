try:
    import http.client
    import urllib.parse
    import time
    import sqlite3
    import requests
    import json
except ImportError:
    print("Import Error") #if imports fail, print this
    


'''def create, this will create 3 different tables: soundsensordata,motionsensordata, lasersensordata'''
def create():
    try:
        c.execute("""CREATE TABLE soundsensordata
                 (NUMERIC soundsensor,soundtime)""") #creates soundsensordata table with 2 columns, soundsensor and its time
        c.execute("""CREATE TABLE motionsensordata
                 (NUMERIC motionsensor,motiontime)""") #creates motionsensordata table with 2 columns, motionsesensor and its time
        c.execute("""CREATE TABLE lasersensordata
                 (NUMERIC lasersensor,lasertime)""") #creates lasersensordata table with 2 columns, motionsensor and its time
        
    except:
        print("Created of tables failed") #if creation of tables fails print this


db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db' #this is where you have saved your database
conn = sqlite3.connect(db_path)
c = conn.cursor()
create() #calles the create method
conn.commit() #commit needed
c.execute('PRAGMA integrity_check;') #database integrity check
c.close() #close database when finished
