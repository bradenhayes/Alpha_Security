import RPi.GPIO as GPIO
import time
import http.client
import urllib.parse
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN)         #Read output from PIR motion sensor
GPIO.setup(3, GPIO.OUT)         #LED output pin
key = "EOOMM9Z3VB6QOGAT"  # Put your API read Key here
count = 0

def motionstatus():
    i=GPIO.input(11)
    assert(i>=0 & i <=1), "Hardware Error"
    if i==0:                 #When output from motion sensor is LOW
        GPIO.output(3, 0)    #Turn OFF LED
        state = "safe"
    elif i==1:               #When output from motion sensor is HIGH
        print ("Intruder detected",i)
        GPIO.output(3, 1)  #Turn ON LED

        count = count + 1
        assert (count > 9999), "Motion Sensor obstructed"
        assert(i>=0 & i <=1), "Hardware Error"
        state = "Intruder Detected"
        params = urllib.parse.urlencode({'field1': i,'key':key })
        headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = http.client.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            data = response.read()
            conn.close()
        except:
            print("connection failed")

if __name__ == "__main__":
    while True:
        motionstatus()