try: 
    import tkinter as tk
    from tkinter import *
    import sqlite3
    import os
    import dropbox
    import webbrowser
    import vlc
    from pydub import AudioSegment
    from pydub.playback import play
    from threading import Thread
    import schedule
    import time
    import http.client
    import urllib.parse
    import time
    import requests
    import json
    import datetime
    from dateutil import parser
    import pytz
    from sys import exit
    from twilio.rest import Client
except ImportError:
    print("Import Error") #if any of the import statements do not import, then this exception handling throws an import error
    
LARGE_FONT= ("Verdana", 12) #font used throughout GUI
ONE_MINUTE=60 #used to compare the time the sensors are tripped to the current time (60 seconds/1 minute)
TWO_MINUTES=120 #used for comparing time to sensors that are tripped  (120 seconds/2 minutes)
CURRENT_STATUS="Safe" #current status of the secruity system
client = Client("ACc5accf5415ccf8712a3bd81278c7e57b", "8fa188fa711e78ce76ce8944efb86af9") #used to connect to Twilio API to send SMS messages


'''class AlphaSecuirty, for actually defining the GUI and making the frame, organizes and initializes all of the different pages
     @param tk.TK, this used for the created of the GUI frame used'''
class AlphaSecurity(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage,CameraStartpage, SecurityPage,PreSubscriptionPage, SubscriptionPage, VideoPage, AudioPage, SensorPage): #all of the posible pages used

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
    #def show_frame, creates and shows the frame for the GUI
    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

'''class StartPage, this is where everything to do with the start page of the GUI will be coded
     @param tk.Frame, this is the frame for the GUI that everything is within'''       
class StartPage(tk.Frame):
    

    def __init__(self, parent, controller):
        #def close, if the quit button is clicked, this method will close the GUI
        def close():
            controller.destroy()
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Alpha Security", font=LARGE_FONT)#label at the top for the title alpha security
        label.pack(pady=10,padx=10) 

        security = tk.Button(self,
                      text ="Security Status",
                      command = lambda: controller.show_frame(SecurityPage)) #Button to direct to security page
        
        subscription = tk.Button(self,
                      text ="Subscription",
                      command = lambda: controller.show_frame(PreSubscriptionPage))#Button to direct to subscription page
        videostream = tk.Button(self,
                   text="Video Stream",
                   fg="blue",
                   command = lambda: controller.show_frame(VideoPage))#Button to direct to videostream page
        audiofiles = tk.Button(self,
                   text="Audio Files",
                   fg="blue",
                   command = lambda: controller.show_frame(AudioPage))#Button to direct to audiofiles page
        sensorhistory = tk.Button(self,
                   text="Sensor History",
                   fg="blue",
                   command = lambda: controller.show_frame(SensorPage))#Button to direct to sensorhistory page
        quitbutton = tk.Button(self,
                   text="QUIT",
                   fg="red",
                   command = close)#Button to direct to close the GUI

        #The remaining code just activates the button on the GUI, this is what ".pack()" does
        security.pack() 
        subscription.pack()

        videostream.pack()
        audiofiles.pack()
        sensorhistory.pack()
        quitbutton.pack()
'''class CameraStartpage is the class where all the code for the start page when the user only has the camera subscription package will be
     @param tk.Frame, this is the frame for the GUI that everything is within'''
class CameraStartpage(tk.Frame):
    

    def __init__(self, parent, controller):
        #def close, this method will be called if the user clicks the quit button and it will close the GUI
        def close(): 
            controller.destroy()
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Alpha Security", font=LARGE_FONT) #label at the top for the title alpha security
        label.pack(pady=10,padx=10)
        
        subscription = tk.Button(self,
                      text ="Subscription",
                      command = lambda: controller.show_frame(PreSubscriptionPage)) #button to acces subscription page
        videostream = tk.Button(self,
                   text="Video Stream",
                   fg="blue",
                   command = lambda: controller.show_frame(VideoPage)) #button to access video stream
        #these two lines of code just activate the buttons in the GUI
        subscription.pack()
        videostream.pack()
'''class SecurityPage, this is where all the code for the security page which gives the current status of the system will be
    will be
    @param tk.Frame, this is the frame for the GUI that everything is within'''
class SecurityPage(tk.Frame):

    def __init__(self, parent, controller):
    
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Security Page", font=LARGE_FONT) #label for the title of page "Security Page"
        label.pack(pady=10,padx=10)

     
        button2 =tk.Button(self,text="Click to get security status",command=self.statuscallback) #this button will call statuscallback and will give the security status of the security system
        button2.pack()#activates button2
        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage)) #button to go back home to the startpage of the GUI
        button1.pack() #activates button1
    #def,popupError this is called whenever there is new sensor activity
    #@param s, this is what will be passed to popupError and it is the current status of the security system
    def popupError(s):
        
        
            popupRoot = Tk() #defining object popupRoot
            popupRoot.after(5000, popupRoot.destroy)#after 2000 milliseconds/200 seconds the notification window will go away
            popupButton = Button(popupRoot, text = s, font = ("Verdana", 12)) #defining the popupbutton for notifications
            popupButton.pack() #activate the popupbutton
            popupRoot.geometry('400x50+700+500') #define location on the screen of popup
            popupRoot.mainloop()
    #def statuscallback, this will be called whenever the button to get the security status is pressed and will give the user the current status of the security system in a messagebox
    def statuscallback(self):
        global CURRENT_STATUS #this is the current status of the system
        messagebox.showinfo(title="Current Security Status",message=CURRENT_STATUS) #messagebox that displays current status of system
        
'''the below class is where all the code for the subscription page that shows 2 options: upgrade and downgrade subscription
     @param tk.Frame, this is the frame for the GUI that everything is within'''
class PreSubscriptionPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Would you like to...", font=LARGE_FONT) #label at the top of the page 
        label.pack(pady=10,padx=10)#activates label

        UpgradeButton = tk.Button(self, text="Upgrade Package",
                            command=lambda: controller.show_frame(SubscriptionPage)) #this is the button for upgrading your subscription package, if clicked it brings you to the scubscription page
        UpgradeButton.pack()#activates button
          
        
        DowngradeButton = tk.Button(self, text="Downgrade Package",
                            command=lambda: controller.show_frame(SubscriptionPage)) #this is the button for downgrading your subscription package, if clicked it brigns you to the subscription page
        DowngradeButton.pack()#activates button
'''class SubscriptionPage, this is where the the code is for the page where the user can actually choose what subscription package they want
    @param tk.Frame, this is the frame for the GUI that everything is within'''        
class SubscriptionPage(tk.Frame):

    def __init__(self, parent, controller):
    
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Subscription Page", font=LARGE_FONT) #label at the top of the page that says "Subscription Page"
        label.pack(pady=10,padx=10)#activates the label
        #the following 6 lines of code are declarations for the variables used to track what radio button is actually selected
        self.controller=controller
        self.cameravar=IntVar()
        self.soundvar=IntVar()
        self.motionvar=IntVar()
        self.laservar=IntVar()
        self.varr=IntVar()
        
        fullbutt=Radiobutton(self,text="Complete Package (Tripwire, Sound security, Motion detection and camera)",variable=self.varr,value=0,command= self.callbackfull) #if this button is clicked then the user will have chosen the full subscription package
        halfbutt=Radiobutton(self,text="Camera Package",variable=self.varr,value=1,command= self.callbackcamera) #if this button is clicked then the user has selected the subscription package that only contains the camera stream
        fullbutt.pack()#activate fullbutt button
        halfbutt.pack()#activate halfbutt button
        button1 = tk.Button(self, text="Home",
                            command=lambda: self.controller.show_frame(StartPage))#this hutton will bring the user to the home page if clicked
        button1.pack() #Will activate button1
    #def callbackfull, this definition will be called if the user selects the radio button for the full package
    #@param self, used to varibale from a different method
    def callbackfull(self):
        self.UpgradeButton=tk.Button(self, text="Click here to confirm upgrade of package",
                                command=lambda: self.controller.show_frame(StartPage)) #this will create the upgrade button 
   
        self.UpgradeButton.pack()#activates the upgradebutton
    
    #def callbackfull, this definition will be called if the user selects the radio button for the camera package
    #@param self, used to varibale from a different method
    def callbackcamera(self):
        self.DowngradeButton=tk.Button(self, text="Click here to confirm downgrade of package",
                                command=lambda: self.controller.show_frame(CameraStartpage)) #this will create the downgrade button
        self.DowngradeButton.pack()#activates the downgradebutton
        
        

'''This class contains all of the code for the VideoPage of the GUI
    @param tk.Frame, this is the frame for the GUI that everything is within'''
class VideoPage(tk.Frame):

    def __init__(self, parent, controller):
        #def Stream this method will be called if the user clicks on the video stream button
        def Stream():
            webbrowser.open_new(r"index.html") #will bring the user to the video stream
            
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Launch Stream", font=LARGE_FONT) #label at top of page for launch stream
        label.pack(pady=10,padx=10) #activate this label
        
        link = tk.Button(self, text="Video Stream",
                            command= Stream) #create button for video stream, this calls method Stream()
        link.pack()#activates this button

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))#activates button that if clicked will bring the user to the home page of the GUI
        button1.pack()#activates this button
'''class AudioPage, this is where all of the code for the Audio page for the GUI will be
    @param tk.Frame, this is the frame for the GUI that everything is within'''
class AudioPage(tk.Frame):

    def __init__(self, parent, controller):
            
        tk.Frame.__init__(self, parent) ##sets up the frame for the page
        label = tk.Label(self, text="Audio Page", font=LARGE_FONT)#label at the top of the page, this sets it up
        label.pack(pady=10,padx=10)#activates label
        #def audioOpen, this is the definition to grab all the audio files from the dropbox app and put them into a file on this raspberry pi, it then makes a button for every individual file with the same name as the file
        def audioOpen():
            try:
                  dbx = dropbox.Dropbox('8WNB4VteJFUAAAAAAAAAAQkkCfn_aeDYNxNuE2p8sIRNh5fWyWuZhLSqwXT5UZ2p') #this the the API code for the dropbox app
                  entries = dbx.files_list_folder('').entries#put every one into a variable
            except:
                  print("Connection to dropbox error") #if connection above to dropbox failed print this error

            for entry in entries:
                if isinstance(entry, dropbox.files.FileMetadata):  #an instance in the entries for the file meta data
                    metadata,f = dbx.files_download(entry.path_lower)
                    out=open(entry.name,'wb')
                    out.write(f.content) #writes every audio file grabbed from dropbox into the same folder that this code is in
            for root, dirs, files in(os.walk("/home/pi/Desktop/Sysc3010/Project/AudioFiles")): #look in this file for 
                    files.sort() #this will sort the files so that they are put in the order of latest to soonest
                    for file in files:
                        if file.endswith(".mp3"): #looks to see if the code ends in .mp3 before it turns it into a button to make sure only the audio files are used
                            f = open(os.path.join(root,file),'rb') #if it is, its saves it as a f object
                            filebutton = tk.Button(self, text=os.path.basename(f.name),
                                command=lambda file=file: play_audio(file)) #this turns every file into its own button and calls play_audio
                            filebutton.pack() #activates filebutton button
                            
        #def play_audio, this will play the audio that is dedicated to that button                 
        def play_audio(file):  
            messagebox.showinfo("", "Playing Audio") #this will pop up to let the user know the audio is playing
            recording= AudioSegment.from_file('/home/pi/Desktop/Sysc3010/Project/AudioFiles/' + str(file)) #will go into the folder that has all of the audio files and then will grab the correct one as "str(file))" will be the name of the file the user wants
            loud_recording = recording +500 #increases the volume of the audio file
            play(loud_recording) #will play this recording
            
            
            
        audiobutton = tk.Button(self, text="Search Directory",
                            command=audioOpen) #button for search directory, will call audioOpen method
        audiobutton.pack()#activates this button
       
        
        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))#button that if clicked will bring the user back to the start page
        button1.pack()#activates this button
'''class SensorPage, this is where the code for the sensor history page will be
    @param tk.Frame, this is the frame for the GUI that everything is within'''
class SensorPage(tk.Frame):

    def __init__(self, parent, controller):
        #def querymotion, this will get all of the sensor data from the motionsensordata chart
        #@param verbose, this is a veriable that is used as a boolean
        def querymotion(verbose=True):
            showdata="" #empty string variable that is used to put the sensor data into
            try:
                db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db' #this is the database where the table is stored
                conn = sqlite3.connect(db_path) #connect to the path and makes it an object conn
                c = conn.cursor() 
                sql = "SELECT * FROM motionsensordata" #selects data from motionsensordata chart
                recs = c.execute(sql)
            except:
                print("connection to database failed") #if connection to database fails then print this
    
            if verbose:
                for row in recs:
                    showdata+=str(row)+ "\n" #will add the sensor history for each row into this variable and then go to the next line
            messagebox.showinfo(title="Motion Sensor History",message=showdata)  #message box that will show all of the motion sensor history 
            c.close() #close the database 
        #def querysound, this will get all of the sensor data from the soundsensordata chart
        #@param verbose, this is a veriable that is used as a boolean
        def querysound(verbose=True):
            showdata="" #empty string variable that is used to put the sensor data into
            try:
                db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db' #this is the database where the table is stored
                conn = sqlite3.connect(db_path) #connects to the path and makes it an object conn
                c = conn.cursor()
                sql = "SELECT * FROM soundsensordata" #selects data from soundsensordata chart
                recs = c.execute(sql)
            except:
                print("connection to database failed") #if connection to database fails then print this
            if verbose:
                for row in recs:
                    showdata+=str(row)+ "\n" #will add the sensor history for each row into this variable and then go to the next line
            messagebox.showinfo(title="Sound Sensor History",message=showdata) #message box that will show all of the sound sensor history  
            c.close() #close the database
        #def querylaser, this will get all of the sensor data from the lasersensordata chart
        #@param verbose, this is a veriable that is used as a boolean   
        def querylaser(verbose=True):
            showdata="" #empty string variable that is used to put the sensor data into
            try:
                db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db' #this is the database where the table is stored
                conn = sqlite3.connect(db_path) #connects to the path and makes it an object conn
                c = conn.cursor()
                sql = "SELECT * FROM lasersensordata" #selects data from lasersensordata chart
                recs = c.execute(sql)
            except:
                print("connection to datbase failed") #if connection to database fails the print this
           
            if verbose:
                for row in recs:
                    showdata+=str(row)+ "\n" #will add the sensor history for each row into this variable and then go to the next line
            messagebox.showinfo(title="Laser Tripwire Sensor History",message=showdata)
            c.close()
        tk.Frame.__init__(self, parent) #frame for this page
        label = tk.Label(self, text="Sensor Page", font=LARGE_FONT) #this is the label for the top of the page
        label.pack(pady=10,padx=10) #activates label
        
        sensorbutton = tk.Button(self, text="See Motion Sensor History",
                            command= querymotion) #button for motion sensor history, if clicked calls querymotion
                            
        sensorbutton.pack() #activates button
        sensorbutton2 = tk.Button(self, text="See Sound Sensor History",
                            command= querysound) #button for sound sensor history, if clicked calls querysound
        sensorbutton2.pack() #activates button
        sensorbutton3 = tk.Button(self, text="See Laser Tripwire Sensor History",
                            command= querylaser) #button for laser sensor histroy, if clicked calls querylaser
        sensorbutton3.pack() #activates button

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage)) #button for home, if clicked brings user back to start page
        button1.pack() #activates button
'''class threatdetect, this class determine the level of threat of the security system based on the sensors'''
class threatdetect:
    #def __init__, initializes all of the variables used within this class
    #@param self, allows the variables to be used throughout all method, and will maintain their values and not be reset
    def __init__(self):
        self.sounddetected=0 #initializes to zero as no sound has been detected
        self.soundtime=0 #initializes to zero as no sound has been detected
        self.laserdetected=0 #initializes to zero as laser has not been tripped
        self.lasertime=0 #initializes to zero as laser has not been tripped
        self.motiondetected=0 #initializes to zero as no motion has been detected
        self.motiontime=0 #initializes to zero as no motion has been detected
        
    #def determinethreat, this method is for multithreading in order to run all of the methods together
    #@param self, used to be able to use variables associated with this object
    def determinethreat(self): 
        f=threatdetect() #create an object f
        soundthingspeak = Thread(target=f.read_sound_thingspeak) #create threading for sound method
        soundthingspeak.start()#start this threading
        soundthingspeak.join()
        laserthingspeak = Thread(target=f.read_laser_thingspeak) #create threading for laser method
        laserthingspeak.start()#start this threading
        laserthingspeak.join()
        motionthingspeak = Thread(target=f.read_motion_thingspeak) #create threading for motion method
        motionthingspeak.start()#start this threading
        motionthingspeak.join()
        fullthreatlevel = Thread(target=f.threatlevel) #create threading for threatlevel method
        fullthreatlevel.start()#start this thread
        fullthreatlevel.join()
        app.after(5000,ah.determinethreat) #will run this method again every 5000 milliseconds/5 seconds, to always check if sensors have been tripped
        
    #def threatlevel, this method determines the level of threat for the security system by comparing sensor inputs and the current time to the time the sensors were tripped at
    #@param self, used to be able to use variables associated with this object
    def threatlevel(self):
        global CURRENT_STATUS #this is to monitor the current status of the security system as a string (which sensors have been tripped)
       
        '''The below code goes through all the possibilities for threat levels for sensors, it will compare the time that the sensor was tripped to the
            current time to determine if the sensor was recently tripped or if it just grabbed an old reading'''
        #the following if statement will check if all 3 of the sensors have been tripped and if they have all been tripped within the last 60 seconds
        if self.laserdetected ==1 and self.sounddetected ==1 and self.motiondetected ==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <ONE_MINUTE:
               if (CURRENT_STATUS== "Threat level 3, all sensors tripped"): #this if statement just makes sure that notifications are not spammed
                   return #return nothing
               else:
                    CURRENT_STATUS= "Threat level 3, all sensors tripped" # all sensors have indeed been tripped
                    
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 3, all sensors tripped") #this will send a text message notification if all sensos have been tripped
                    except:
                        print("sms failed to send") #if sms failed to send print
                    ahh.popupError("Threat level 3") #popup notification if all sensors have been tripped
       
        #the following elif statement will check if both the laser has been broken and sound have been detected and if they have both happened within the last minute
        elif self.laserdetected == 1 and self.sounddetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <ONE_MINUTE:
                if(CURRENT_STATUS== "Threat level 2,laser has been broken and sound has been detected too please listen to most recent audio file"): #this if statement just makes sure notifications are not spammed
                    return #return nothing
                elif (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <TWO_MINUTES: #this elif just makes sure that once one sensor is out of the 60 second range but the other isnt, that it does not change the threat level
                    return #return nothing
                else:
                    CURRENT_STATUS= "Threat level 2,laser has been broken and sound has been detected too please listen to most recent audio file" #if both the sensors have been tripped then update current status
                    
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 2, laser has been broken and sound has been detected") #this will send an SMS notification 
                    except:
                        print("sms failed to send") #if sms failed to send print
                    ahh.popupError("Threat level 2, laser has been broken and sound has been detected") #will give a popup notification
        #the following elif statement will check if both the motion sensor and sound sensor have been tripped               
        elif self.motiondetected == 1 and self.sounddetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <ONE_MINUTE:
                if(CURRENT_STATUS=="Threat level 2, motion has been detected and so has sound please listen to most recent audio file"): #this if statement just makes sure notifications are not spammed
                    return #return nothing
                elif (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <TWO_MINUTES:#this elif just makes sure that once one sensor is out of the 60 second range but the other isnt, that it does not change the threat level
                    return #return nothing
                else:
                    CURRENT_STATUS="Threat level 2, motion has been detected and so has sound please listen to most recent audio file" #if both sensors have been tripped then update current status
                    
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 2, motion and sound have been detected") #this will send an SMS notification
                    except:
                        print("sms failed to send")
                    ahh.popupError("Threat level 2, motion and sound have been detected")  #will give a popup notification
        #the following elif statement will check if both motion has been sensed and if the laser has been tripped and if both happened within the last 60 seconds           
        elif self.motiondetected == 1 and self.laserdetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE:
                if( CURRENT_STATUS=="Threat level 2, motion has been detected and laser has been tripped"): #this if just makes sure that notifications are not spammed
                    return #return nothing
                elif (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <TWO_MINUTES:#this elif just makes sure that once one sensor is out of the 60 second range but the other isnt, that it does not change the threat level
                    return #return nothing
                else:
                    CURRENT_STATUS="Threat level 2, motion has been detected and laser has been tripped" #if both sensor have been tripped update current status
                    
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 2, motion has been detected and laser has been tripped") #this will send an SMS notification
                    except:
                        print("sms failed to send") #if sms failed to send print
                    ahh.popupError("Threat level 2, motion has been detected and laser has been tripped") #will give a popup notification
        #the following elif statement will check if sound has been sensed and if it was within the last 60 seconds            
        elif self.sounddetected==1 and(datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds()<ONE_MINUTE:
                if(CURRENT_STATUS=="Threat level 1, sound has been detected please listen to most recent audio file"): #this if statement just makes sure that notifications are not spammed
                    return #return nothing
                #the following elif just makes sure that once one sensor is out of the 60 second range but the other isnt, that it does not change the threat level
                elif (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <TWO_MINUTES or (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <TWO_MINUTES:
                    return #return nothing
                else:
                    CURRENT_STATUS="Threat level 1, sound has been detected please listen to most recent audio file" #if sound was sensed update current status
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 1, sound has been detected") #this will send an SMS notification
                    except:
                        print("sms failed to send") #if sms failed to send print
                    ahh.popupError("Threat level 1, sound has been detected") #will give a popup notification
                    
        #the following elif statement will check if the tripwire has broken and if it was within the last 60 seconds
        elif self.laserdetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE:
                if(CURRENT_STATUS=="Threat level 1, tripwire has been broken"): #this if statement just makes sure that notifications are not spammed
                    return #return nothing
                elif (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <TWO_MINUTES or (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds()<TWO_MINUTES:
                    return #return nothing
                else:
                     CURRENT_STATUS="Threat level 1, tripwire has been broken" #if tripwire was broken update current status
                     try:
                         client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 1, tripwire has been broken") #this will send an SMS notification
                     except:
                        print("sms failed to send") #if sms failed to send print
                     ahh.popupError("Threat level 1, tripwire has been broken") #this will give a popup notification
                    
        #the following elif statement will check if motion has been detected and if it was within the last 60 seconds
        elif self.motiondetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE:
                if(CURRENT_STATUS=="Threat level 1, motion has been detected"): #this if statement just makesa sure that notifications are not spammed
                    return #return nothing
                #this elif just makes sure that once one sensor is out of the 60 second range but the other isnt, that it does not change the threat level
                elif (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <TWO_MINUTES or (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds()<TWO_MINUTES:
                    return #return nothing
                
                else:
                    CURRENT_STATUS="Threat level 1, motion has been detected" #if motion has been detected update current status
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 1, motion has been detected") #this will send an SMS notification
                    except:
                        print("sms failed to send") #if sms failed to send print
                    ahh.popupError("Threat level 1, motion has been detected") #this will give a popup notification
                    
        else: #if no sensor activity then enter this else statement
               if(CURRENT_STATUS != "Safe"):
                   time.sleep(60) #this is to make sure that it does not say safe too early
                   CURRENT_STATUS = "Safe"
               else:
                   CURRENT_STATUS ="Safe" #if no sensors have been tripped within the last 60 seconds then update current status to safe
                  
    #def read_sound_thingspeak, this method will read the sensor data from thingspeak and save the sensor status and its corresponding time and will the put it in the database
    #@param self, this is to be able to use variables associated with this object
    def read_sound_thingspeak(self):
        db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db' #this is the database path
        conn = sqlite3.connect(db_path) #connect to the database
        c = conn.cursor()
        soundURL='https://api.thingspeak.com/channels/1152850/fields/1.json?api_keys=' #thingspeak url for soundsensor channel
        soundKEY='8T5J8V8E0LX16RY5' #read api key for channel
        soundHEADER='&results=1'  #we want the most recent result that was written to the channel
        sound_FULL=soundURL+soundKEY+soundHEADER #combine to be able to get the data
        soundresults=requests.get(sound_FULL).json()
        data=[]#create an array to store results
        try:
            for x in soundresults['feeds']: #look in the feeds of the json
                data.insert(0,int(x['field1'])) #put the field 1 value into the first element of the array data
                self.sounddetected = data[0] #make this value equal to self.sounddetected
            for x in soundresults['feeds']: #look in the feeds of the json
                data.insert(1,str(x['created_at'])) #put the created_at value into the second element of the array data
                self.soundtime=data[1] #make this value equal to self.soundtime
        except:
            print("failed to read from SoundSensor Thingspeak") #if connection/reading with thingspeak failed, print this
        try:
            sql = "SELECT * FROM soundsensordata ORDER BY soundtime DESC LIMIT 1" #select data from soundsensordata in order
            recs = c.execute(sql)
            if True:
                for row in recs:
                 
                
                     if row != (1, self.soundtime):    #to avoid duplicate values in table
                            c.execute("""INSERT INTO soundsensordata VALUES(?,?)""", 
                                    (self.sounddetected,self.soundtime)) #insert values into chart
                conn.commit() #commit needed
        except:
            ("Failed to insert into soundsensordata table") #if insert into table failed then print this
        c.close() #close database 
    #def read_laser_thingspeak, this method will read the sensor data from thingspeak and save the sensor status and its corresponding time and will the put it in the database
    #@param self, this is to be able to use variables associated with this object
    def read_laser_thingspeak(self):
        
        db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db' #get the database we want
        conn = sqlite3.connect(db_path) #connect to the database
        c = conn.cursor()
        laserKEY='QEAI32EFVL4ZM7ZR' #read api key for laser tripwire channel
        laserURL= 'https://api.thingspeak.com/channels/1150122/fields/1.json?api_key=' #url for the thingspeak channel
        laserHEADER ='&results=1' #we want this most recent data point that has been written to channel
        laser_FULL = laserURL+laserKEY+laserHEADER
        laserresults=requests.get(laser_FULL).json()
        data2=[] #array to store the data
        try:
            for x in laserresults['feeds']: #look in the feeds of the json
                data2.insert(0,int(x['field1'])) #insert field1 into the array at the first element
                self.laserdetected = data2[0] #make this value equal to self.laserdetected
            for x in laserresults['feeds']: #look in the feeds of the json
                data2.insert(1,str(x['created_at'])) #insert created_at into the array at the second element
                self.lasertime=data2[1] #make this value equal to self.lasertime
        except:
            print("failed to read from laser tripwire Thingspeak") #if connection or read with thingspeak failed, then print this
        try:
            sql = "SELECT * FROM lasersensordata ORDER BY lasertime DESC LIMIT 1" #select data from lasersensordata in order
            recs = c.execute(sql)
            if True:
                for row in recs:
                 
                     if row != (1, self.lasertime ):    #this is to avoid duplicate values in chart
                            c.execute("""INSERT INTO lasersensordata VALUES(?,?)""",
                                  (self.laserdetected,self.lasertime)) #insert values into lasersensordata table
                conn.commit() #commit needed
        except:
            print("failed to insert into lasersensordata table") #if insertion into table failed, then print this
        c.close() #close database
        
    #def read_motion_thingspeak, this method will read the sensor data from thingspeak and save the sensor status and its corresponding time and will the put it in the database
    #@param self, this is to be able to use variables associated with this object    
    def read_motion_thingspeak(self):
        
        db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db' #this is the database we want to connect to
        conn = sqlite3.connect(db_path) #connect to this database
        c = conn.cursor()
        motionURL='https://api.thingspeak.com/channels/1219425/fields/1.json?api_key=' #url for the motion sensor thingspeak channel
        motionKEY='GQ6EDK3P60AS7YLO' #read api key for this channel
        motionHEADER='&results=1' #we want the most recent data point written to this channel
        motion_FULL=motionURL+motionKEY+motionHEADER
        motionresults=requests.get(motion_FULL).json()
        data3=[] #creat array to store values
        try:
            for x in motionresults['feeds']: #look into the feeds of motionresults
                data3.insert(0,int(x['field1'])) #insert field1 value into array at the first element
                self.motiondetected=data3[0] #make this value equal to self.motiondetected
            for x in motionresults['feeds']: #look into the feeds of motionresult
                data3.insert(1,str(x['created_at'])) #insert created_at value into array at the second element
                self.motiontime=data3[1] #make this value equal to self.motiondeteceted
        except:
            print("failed to read from motion Thingspeak") #if connection/read with thingspeak failed, print this
        try:
            sql = "SELECT * FROM motionsensordata ORDER BY motiontime DESC LIMIT 1" #select data from motionsensordata in order
            recs = c.execute(sql)
            if True:
                for row in recs:
                
                     if row != (1, self.motiontime ): #this is to avoid duplicate data in the table
                            c.execute("""INSERT INTO motionsensordata VALUES(?,?)""",
                                  (self.motiondetected,self.motiontime)) #insert data into table
                conn.commit() #commit needed
        except:
            print("failed to insert into motionsensordata table") #if insertion into table failed, print this
        c.close() #close database
ahh=SecurityPage #create object ahh
ah=threatdetect() #create object ah
app = AlphaSecurity() #create object app
app.title("Security System Control Console") #give GUI a title
app.after(5000,ah.determinethreat) #run determinethreat after 5 seconds
app.mainloop() 
