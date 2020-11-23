#Alpha Security
#SYSC 3010
#Riley Johnston 101088019

import os
import subprocess
import time
import multiprocessing

def testProcess():
    #internetConnection.py is the script that streams video to AWS when internet is available and saves video to local storage when internet goes down
    #Call the script.  This is the code under test.
    subprocess.call(["python3", "internetConnection.py"])
    #subprocess.Popen("internetConnection.py", close_fds=True)

videoTestProcess = multiprocessing.Process(target=testProcess)
videoTestProcess.start()

#Let the script run for a few seconds.  It is streaming video to AWS. 
time.sleep(6)

#Cut off internet connection so that the code begins storing footage locally.
os.system("sudo rfkill block wifi")

time.sleep(15)

#Reactivate Wifi after 15 seconds.  Video Will stop storing locally and resume streaming to AWS.
os.system("sudo rfkill unblock wifi")

time.sleep(6)

videoTestProcess.terminate()
videoTestProcess.join()

#The video file will be the most recently edited file
#obtain the filename of the file with most recent date-stamp
path = os.getcwd()
files = os.listdir(path)
latestFile = max(files, key = os.path.getctime)

#Open the video
subprocess.call(["xdg-open", str(latestFile)])
