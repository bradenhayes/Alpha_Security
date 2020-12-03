#Alpha Security
#SYSC 3010
#Riley Johnston 101088019

#This script streams video to AWS while internet connection is available
#When internet connection is unavailable, video files are saved to local SD card storage

import urllib.request
import time
import multiprocessing
import subprocess
import os
import picamera
import datetime

stream_running_g = False

def startStream():
    #stream video from raspberry pi camera to the AWS Kinesis streaming server  
    streamPID = os.getpid()
    print("stream PID: " + str(streamPID))
    print("LAUNCHING STREAM")
    #Initiate the video stream to AWS
    #This beings delivery of the video taken by the local raspberry pi camera through a gstreamer pipeline to a kvssink where it connects to the AWS Kinesis SDK for upload to the server
    subprocess.Popen(["bash", "startStream.sh"])

def killTargetProcess(target_process):
    #Kill a process by name
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
    #Check internet connection every two seconds
    #If internet is lost, terminate video upload process and begin storing locally
    #When internet becomes available, resume live stream to AWS
    global stream_running_g
    global videoStreamProcess
    while(True):
        print("2")
        if not connect():
            print("Internet Lost")
            #Check if the video stream thread process is active.  If so, terminate the video streaming thread process
            if videoStreamProcess.is_alive():
                print("terminate process")
                killTargetProcess("gst-launch-1.0")
                currentDate = datetime.datetime.now()
                camera.start_recording(str(currentDate) + ".h264")
                videoStreamProcess.terminate()
                videoStreamProcess.join()
                stream_running_g = False
        else:
            print("internet connected")
            #Check if the video stream process is active.  If so, activate the the video streaming processm
            if not videoStreamProcess.is_alive():
                print("Internet now availabe.  Resuming video stream...")
                videoStreamProcess = multiprocessing.Process(target=startStream)
                videoStreamProcess.start()
                camera.stop_recording()
                stream_running_g = True
        time.sleep(2)
        

def connect(host='http://google.com'):
    #Ping google
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

camera = picamera.PiCamera()

#Launch the video streaming process
videoStreamProcess = multiprocessing.Process(target=startStream)
videoStreamProcess.start()
#startStream()
#From the main process, monitor the internet connection
checkInternetConnection()
