try:
    import RPi.GPIO as GPIO
    import time
    import http.client
    import urllib.parse
    import sounddevice as sd
    from scipy.io.wavfile import write
    from pydub import AudioSegment
    import os
    import dropbox
    from threading import Thread
    import datetime
    from multiprocessing import Process
    import numpy as np
    import glob
except ImportError:
    print("Import Error") #if imports fail, print this



timeah='i' #used incase there are 2 recordings saved with the same name      
key = "H9WE4FP198D1A2M9"  # Thingspeak API write key
fs = 44100  # Sample rate
testduration=1 #length of test recording
duration =5 #Length of recording
myrecordings=[] #array used for insert of audio recordings
dbx = dropbox.Dropbox('Tf6ZkhYdVW0AAAAAAAAAASbGkKs9SB5BxP2k4ZeYnzgIzlpIiUBkMhpVWu3J-coB') #dropbox API key
dbx.users_get_current_account() 

#GPIO SETUP
channel = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

'''The following code tests upon startup if the mic is connected and working by recording a one second clip, saving it to a directory,
checking if the file was saved and exists, then removing that file'''

myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1) #record for 1 second
sd.wait()  # Wait until recording is finished
write('test.mp3', fs, myrecording) #save the recording as test.mp3

for file in os.listdir("/home/pi/Desktop/Sysc3010/Project/FolderForFinal"): #look in this folder
    if "test.mp3" in file: #if test.mp3 is there
        print("yes usb mic is connected") #prin this is test.mp3 is found, meaning usb mic is connected and working

os.remove("/home/pi/Desktop/Sysc3010/Project/FolderForFinal/test.mp3")#remove this file


'''define recording, recording will constantly be recording 5 seconds clips, and saving them to a folder, everytime it records one it will increment
    recording so that it says a different file name'''
def record():
    i=0 #used for array insertion
    recording = 'i' #used to change the name of the recording each time
    while True:
         
         myrecordings.insert(i, sd.rec(int(duration * fs), samplerate=fs, channels=1)) #record 10 second clips and put them into elements of the array
         sd.wait() #wait till recording is finished
         write(recording +'.mp3',fs,myrecordings[i]) #save file to folder
         recording += 'i' #change name of recording string
         i+=1 #increment i by 1 to insert into next value of array
         
'''define callback, will be called whenever the sound sensor detect sound, it will upload the most recent audio file to dropbox (containing the sound)
    and then will write the sensor data to thingspeak
        @param channel, this is the GPIO pin that is used'''
def callback(channel):
        global timeah
        if GPIO.input(channel): #if input
                channel =17 #channel is 17
        else:
                print ("Sound Detected!") #if input, print this
                list_of_files = glob.glob('/home/pi/Desktop/Sysc3010/Project/FolderForFinal/*.mp3') #using glob we grab the most recent file that ends in .mp3 from this directory
                latest_file = max(list_of_files, key=os.path.getctime)
                f= open(latest_file,'rb') #open the file and store it as an object f
                dbx.files_upload(bytes(f.read()),'/'+ datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y" + timeah + '.mp3'))#Names the file the current time #this will write the file to dropbox and name it the current time
                timeah += 'i' #increment variable by i
                
                params = urllib.parse.urlencode({'field1': 1, 'key':key }) #connecting to thingspeak
                headers = {"Content-typZZe": "application/x-www-form-urlencoded","Accept": "text/plain"}
                conn = http.client.HTTPConnection("api.thingspeak.com:80")
                conn.request("POST", "/update", params, headers) #writing to thingspeak
                try:
                
                    response = conn.getresponse()
                    data = response.read() #writing to thingspeak
                    conn.close()
                    time.sleep(1)
                except:
                    print("ahh") #if writing to thingspeak failed call this
'''The following GPIO lines add the events for the callback function'''
GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
GPIO.add_event_callback(channel, callback)  # assign function to GPIO PIN, Run function on change

if __name__ == '__main__':
    time.sleep(1)
    record()
