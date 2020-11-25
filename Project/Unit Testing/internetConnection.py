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
    try:
        streamPID = os.getpid()
        print("stream PID: " + str(streamPID))
        print("LAUNCHING STREAM")
        #Initiate the video stream to AWS
        #This beings delivery of the video taken by the local raspberry pi camera through a gstreamer pipeline to a kvssink where it connects to the AWS Kinesis SDK for upload to the server
        subprocess.run("gst-launch-1.0 v4l2src do-timestamp=TRUE device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! omxh264enc control-rate=1 target-bitrate=5120000 periodicity-idr=45 inline-header=FALSE ! h264parse ! video/x-h264,stream-format=avc,alignment=au,width=640,height=480,framerate=30/1,profile=baseline ! kvssink stream-name='SecurityCamera' access-key='AKIAVMRNWFLTQ7RTPWOQ' secret-key='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' aws-region='us-east-2'", shell=True)
    except:
        print("error detected")

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

#From the main process, monitor the internet connection
checkInternetConnection()
