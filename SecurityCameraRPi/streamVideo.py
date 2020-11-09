#This code sets up and begins the video stream from Raspberry pi camera to AWS Kinesis Video Streaming Server
#If the local network becomes (or is at any time) unavailable, video footage is stored locally


import subprocess
import time

subprocess.run("gst-launch-1.0 v4l2src do-timestamp=TRUE device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! omxh264enc control-rate=1 target-bitrate=5120000 periodicity-idr=45 inline-header=FALSE ! h264parse ! video/x-h264,stream-format=avc,alignment=au,width=640,height=480,framerate=30/1,profile=baseline ! kvssink stream-name='SecurityCamera' access-key='AKIAVMRNWFLTQ7RTPWOQ' secret-key='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' aws-region='us-east-2'")
print("1")
try:
    #time.sleep(3)
    subprocess.run("gst-launch-1.0 v4l2src do-timestamp=TRUE device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! omxh264enc control-rate=1 target-bitrate=5120000 periodicity-idr=45 inline-header=FALSE ! h264parse ! video/x-h264,stream-format=avc,alignment=au,width=640,height=480,framerate=30/1,profile=baseline ! kvssink stream-name='SecurityCamera' access-key='AKIAVMRNWFLTQ7RTPWOQ' secret-key='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' aws-region='us-east-2'")
except:
    print("error detected")
