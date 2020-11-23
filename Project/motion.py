import RPi.GPIO as GPIO
import time
import http.client
import urllib.parse
from datetime import datetime
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin
key = "EOOMM9Z3VB6QOGAT"        #Put your API read Key here
location = None

def motionstatus():
    i=GPIO.input(11)
    if location==None:
        print ("WARNING: Location Data not available")

    assert(i>=0 & i <=1), "Hardware Error"
    if i==0:                 #When output from motion sensor is LOW
        GPIO.output(3, 0)    #Turn OFF LED
        state = "safe"
    elif i==1:               #When output from motion sensor is HIGH
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print ("Intruder detected:", current_time)
        print ("Location: ", location)
        GPIO.output(3, 1)  #Turn ON LED


        assert(i>=0 & i <=1), "Hardware Error"
        state = "Intruder Detected"
        params = urllib.parse.urlencode({'field1': "Motion Detected",'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except:
            print("connection failed")
        time.sleep(3)

if __name__ == "__main__":
    while True:
        print ("Press M to move motion sensor")
        print ("Press E to enable motion sensor")
        movekey = input();
        if movekey =="M":
            location = input("What is the location?")
        elif movekey == "E":
            while True:
                motionstatus()
