#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import http.client
import urllib.parse

GPIO.setmode(GPIO.BCM)
GPIO.setup(14,GPIO.IN)

key = "FJCOCAFQMNLMO463"

def tripwire():
    if GPIO.input(14) == GPIO.HIGH:
        print("safe")
    elif GPIO.input(14) == GPIO.LOW:
        print (GPIO.input(14))
        print ("Intruder")
        params = urllib.parse.urlencode({'field1': "intruder", 'key':key }) 
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        start_time = time.time()
        elapsed_time = time.time() - start_time
        
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except:
            print ("connection failed")



if __name__ == "__main__":
    while True:
            tripwire()

GPIO.cleanup()

