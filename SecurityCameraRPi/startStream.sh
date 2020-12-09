# Alpha Security
# SYSC 3010
# Riley Johnston

# This command initiates frame transfer through the gstreamer pipeline
# See AWS Kinesis tutorial at https://docs.aws.amazon.com/kinesisvideostreams/latest/dg/producersdk-cpp-rpi.html 

gst-launch-1.0 v4l2src do-timestamp=TRUE device=/dev/video0 ! videoconvert ! video/x-raw,format=I420,width=640,height=480,framerate=30/1 ! omxh264enc control-rate=1 target-bitrate=5120000 periodicity-idr=45 inline-header=FALSE ! h264parse ! video/x-h264,stream-format=avc,alignment=au,width=640,height=480,framerate=30/1,profile=baseline ! kvssink stream-name='SecurityFootage' access-key='AKIAVMRNWFLT5YQDSY46' secret-key='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' aws-region='us-east-2'
