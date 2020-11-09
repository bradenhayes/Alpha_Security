#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import http.client
import urllib.parse
import time
pin=17;
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)        
key = "H9WE4FP198D1A2M9"  # Put your API read Key here

def soundsensed():
    assert(GPIO.input(17)>=0& GPIO.input(17)<=1)
    if GPIO.input(17)==GPIO.LOW:
            
            print ("Sound Detected!")
            params = urllib.parse.urlencode({'field1': 1, 'key':key })
            headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
            conn = http.client.HTTPConnection("api.thingspeak.com:80")
            try:
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                data = response.read()
                conn.close()
                time.sleep(1)
            except:
                print("connection failed")
                


if __name__ == "__main__":
    while True:
        soundsensed()
