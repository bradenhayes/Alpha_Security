#Alpha Security
#SYSC 3010
#Riley Johnston 101088019

import urllib.request
import time
import multiprocessing
import subprocess
import os
import picamera
import datetime

stream_running_g = False
streamPID = -1

def startStream():
    try:
    #time.sleep(3)
        #while(True):
        #print("1")
        #time.sleep(0.5)
        streamPID = os.getpid()
        print("stream PID: " + str(streamPID))
        print("LAUNCHING STREAM")
        while (True):
            time.sleep(1)
            print("Streaming Video...")
        #subprocess.run("gst-launch-1.0 v4l2src do-timestamp=TRUE device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! omxh264enc control-rate=1 target-bitrate=5120000 periodicity-idr=45 inline-header=FALSE ! h264parse ! video/x-h264,stream-format=avc,alignment=au,width=640,height=480,framerate=30/1,profile=baseline ! kvssink stream-name='SecurityCamera' access-key='AKIAVMRNWFLTQ7RTPWOQ' secret-key='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' aws-region='us-east-2'", shell=True)
    except:
        print("error detected")

def killTargetProcess(target_process):
    target_process = str(target_process)
    print("KILL TARGET PROCESS " + target_process)
    subp = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    output, error = subp.communicate()
    print(output)
    for line in output.splitlines():
        if target_process in str(line):
            pid = int(line.split(None, 1)[0])
            os.kill(pid, 9)
        
def checkInternetConnection():
    global PID
    global stream_running_g
    global videoStreamProcess
    while(True):
        print("2")
        if not connect():
            print("Internet Lost")
            #Check if the video stream thread process is active.  If so, terminate the video streaming thread process
            if videoStreamProcess.is_alive():
                print("terminate process")
                #videoStreamProcess.suspend()
                #os.kill(int(PID), 9)
                #print("killed PID: " + str(PID))
                killTargetProcess("gst-launch-1.0")
                currentDate = datetime.datetime.now()
                camera.start_recording(str(currentDate) + ".h264")
                videoStreamProcess.terminate()
                videoStreamProcess.join()
                stream_running_g = False
        else:
            print("still connected")
            #Check if the video stream process is active.  If so, activate the the video streaming processm
            if not videoStreamProcess.is_alive():
                print("ya")
                videoStreamProcess = multiprocessing.Process(target=startStream)
                videoStreamProcess.start()
                camera.stop_recording()
                stream_running_g = True
        time.sleep(2)
        

def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

camera = picamera.PiCamera()
videoStreamProcess = multiprocessing.Process(target=startStream)

videoStreamProcess.start()
#time.sleep(1)
checkInternetConnection()

time.sleep(15)

print("game over")
killTargetProcess("gst-launch-1.0")
videoStreamProcess.terminate()
videoStreamProcess.join()
