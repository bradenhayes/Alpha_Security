#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import http.client
import urllib.parse

pin = 14;

GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.IN)

key = "FJCOCAFQMNLMO463"

def tripwire():
    if GPIO.input(14) == GPIO.HIGH:
        return
    elif GPIO.input(14) == GPIO.LOW:
        print ("Intruder")
        params = urllib.parse.urlencode({'field1': 1, 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except:
            print ("connection failed")

def tester():
    start = time.time()
    if GPIO.input(14) == GPIO.HIGH and time.time() > 10:
        return 1



if __name__ == "__main__":
    while True:
            tripwire()
            tester()

GPIO.cleanup()

