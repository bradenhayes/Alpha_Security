# SYSC3010_L2_M12

## Overview of Alpha Security
The Alpha Security Security System provides remote monitoring of a residence

Keeping your home safe is top priority for us at Alpha Security and to do this we have implemented a full security system built from 4 raspberry Pis that will monitor your house 24/7. This security system is composed of a 1080p video camera for viewing all residential activity, an infrared motion detector for detecting any unwanted guests, a  sound sensor with audio to record what is happening at the residence and detect any forced entries whether that is through the front door or through the breaking of a window and a laser tripwire for detecting any entries. This full composition allows for a complete security system to cover all areas of entry into a residence.  

Our system allows for additional sensors to be added as they are all controlled by the same standalone raspberry pi. For houses that have more than one main entrance, they may want to have an additional tripwire or an additional camera. Not only can users add more sensors but Alpha Security also offers packages for those that may not need the entire package and may just want the camera and tripwire for example. 

The security system allows users to monitor their house from anywhere with the Alpha Security app. Along with this, the 4th raspberry pi will be the server for the security system which will work on a monitor with Alpha Security’s very own desktop GUI.


## Desciption of the major code components

### Android Application (AlphaSecurityApp)
The andriod app allows a homeowner to remotely monitor their residence(s).  When a breakin is detected (one or more sensors triggered), the homeowner is notified of the situation by an SMS message.  He may then open the AlphaSecurity app and, onced logged in, watch the live stream through the security camera.  
Google Firebase is used for account authorization.  New users may be registered through the application.   

### Desktop Application (GUI)
the 4th raspberry pi will be the server for the security system which will work on a monitor with Alpha Security’s desktop applicatio. This desktop application also gives popup notifications and will store all of the sensor data in a database which is readily available to be viewed by the user. The desktop will also store all of the audio files which can be played whenever the user wishes with the click of a button. All of the sensor data will always be time stamped and this is the same case for the audio files.


### Sensor controlling scripts and unit tests (Project)


### Video Stream Producer (SecurityCameraRPi)

Security camera video stream is uploaded to AWS from the RPi controlling the camera.  This is implemented by two concurrently executing Python processes.  The first process streams footage to AWS.  The second process pings google every 2 seconds.  As long as internet is available it allows the streaming to continue.  If at any point, it detects that the internet is down, it terminates the process that streams to AWS, and instead begins recording MP4 video and storing it locally.  Every two seconds, it continues checking network connection, and if at any point the connection is re-established, it relaunches the process that streams to AWS.  This way a homeowner can go back and review footage from when the internet was down.

A gstreamer pipeline is set up by the build script to transfer video frames from the camera to to the kvssink element (also set up by the build script) to deliver video fragments to AWS using the Kinesis SDK (code for SDK cloned from git in build script).