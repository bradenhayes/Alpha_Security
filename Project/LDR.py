#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import http.client
import urllib.parse

pin = 14;# sets pin to 14 which is the one plugges in to the rip

GPIO.setmode(GPIO.BCM) #sets pin to be ready
GPIO.setup(pin,GPIO.IN) #pin is set and now 14

key = "FJCOCAFQMNLMO463" #thingspeak write key

def tripwire():
    if GPIO.input(14) == GPIO.HIGH: #if there is current running throught the system due to the laser the tripwire is not broken and armed
        return
    elif GPIO.input(14) == GPIO.LOW: #when current stops running throught the tripwire is broken and will now send a one to thingspeak
        print ("Intruder")
        params = urllib.parse.urlencode({'field1': 1, 'key':key }) #writing to thingspeak
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except:
            print ("connection failed")#if unsuccessful print conenction failed

def tester(): #hardware test to ensure tripwire is working correctly after 10 second it prints statment
    start = time.time()
    if GPIO.input(14) == GPIO.HIGH and time.time() > 10:
        return 1



if __name__ == "__main__":
    while True:
            tripwire()#runs thingspeak 
            tester()#runs hardware test

GPIO.cleanup()

