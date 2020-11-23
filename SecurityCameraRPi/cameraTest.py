#Alpha Security
#SYSC 3010
#Riley Johnston 101088019

from picamera import PiCamera
import subprocess

camera = PiCamera()
camera.capture("testImage.jpg")
subprocess.run(["xdg-open","testImage.jpg"])
