#Alpha Security
#SYSC 3010
#Riley Johnston

#Hardware Test
#This script validates that the raspberry pi camera is connected properly and is operational
#This script takes a picture and opens it on the raspberry pi

from picamera import PiCamera
import subprocess

camera = PiCamera()
camera.capture("testImage.jpg")
subprocess.run(["xdg-open","testImage.jpg"])
