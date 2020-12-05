try: 
    import tkinter as tk
    from tkinter import *
    from tkinter import Tk, BOTH, messagebox
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
    import sqlite3
    import datetime
    from dateutil import parser
    import pytz
    from sys import exit
    from twilio.rest import Client
except ImportError:
    print("Import Error") #if any of the import statements do not import, then this exception handling throws an import error
    
LARGE_FONT= ("Verdana", 12) #font used throughout GUI
ONE_MINUTE=60 #used to compare the time the sensors are tripped to the current time (60 seconds/1 minute)
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

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage)) #button to go back home to the startpage of the GUI
        button1.pack() #activates button1
        button2 =tk.Button(self,text="Click to get security status",command=self.statuscallback) #this button will call statuscallback and will give the security status of the security system
        button2.pack()#activates button2
    #def,popupError this is called whenever there is new sensor activity
    #@param s, this is what will be passed to popupError and it is the current status of the security system
    def popupError(s):
            popupRoot = Tk() #defining object popupRoot
            popupRoot.after(2000, exit)#after 2000 milliseconds/200 seconds the notification window will go away
            popupButton = Button(popupRoot, text = s, font = ("Verdana", 12), command = exit) #defining the popupbutton for notifications
            popupButton.pack() #activate the popupbutton
            popupRoot.geometry('400x50+700+500') #define the size of it
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
        
class AudioPage(tk.Frame):

    def __init__(self, parent, controller):
            
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Audio Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        def audioOpen():
            try:
                  dbx = dropbox.Dropbox('8WNB4VteJFUAAAAAAAAAAQkkCfn_aeDYNxNuE2p8sIRNh5fWyWuZhLSqwXT5UZ2p')
                  entries = dbx.files_list_folder('').entries
            except:
                  print("Connection to dropbox error")

            for entry in entries:
                if isinstance(entry, dropbox.files.FileMetadata):  
                    metadata,f = dbx.files_download(entry.path_lower)
                    out=open(entry.name,'wb')
                    out.write(f.content)
            for root, dirs, files in(os.walk("/home/pi/Desktop/Sysc3010/Project/AudioFiles")):
                    files.sort()
                    for file in files:
                        if file.endswith(".mp3"):
                            f = open(os.path.join(root,file),'rb')
                            filebutton = tk.Button(self, text=os.path.basename(f.name),
                                command=lambda file=file: play_audio(file))
                            filebutton.pack()
        def play_audio(file):
            messagebox.showinfo("Button label", file)
            recording= AudioSegment.from_file('/home/pi/Desktop/Sysc3010/Project/AudioFiles/' + str(file))
            loud_recording = recording +500
            play(loud_recording)
            
            
            
        audiobutton = tk.Button(self, text="Search Directory",
                            command=audioOpen)
        audiobutton.pack()
       
        
        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
class SensorPage(tk.Frame):

    def __init__(self, parent, controller):
        def querymotion(verbose=True):
            showdata=""
            try:
                db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db'
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                sql = "SELECT * FROM motionsensordata"
                recs = c.execute(sql)
            except:
                print("connection to database failed")
    
            if verbose:
                for row in recs:
                    showdata+=str(row)+ "\n"
            messagebox.showinfo(title="Sound Sensor History",message=showdata)    
            c.close()
        def querysound(verbose=True):
            showdata=""
            try:
                db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db'
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                sql = "SELECT * FROM soundsensordata"
                recs = c.execute(sql)
            except:
                print("connection to database failed")
            if verbose:
                for row in recs:
                    showdata+=str(row)+ "\n"
            messagebox.showinfo(title="Sound Sensor History",message=showdata)        
            c.close()
        def querylaser(verbose=True):
            showdata=""
            try:
                db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db'
                conn = sqlite3.connect(db_path)
                c = conn.cursor()
                sql = "SELECT * FROM lasersensordata"
                recs = c.execute(sql)
            except:
                print("connection to datbase failed")
           
            if verbose:
                for row in recs:
                    showdata+=str(row)+ "\n"
            messagebox.showinfo(title="Laser Tripwire Sensor History",message=showdata)
            c.close()
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sensor Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        sensorbutton = tk.Button(self, text="See Motion Sensor History",
                            command= querymotion)
                            
        sensorbutton.pack()
        sensorbutton2 = tk.Button(self, text="See Sound Sensor History",
                            command= querysound)
        sensorbutton2.pack()
        sensorbutton3 = tk.Button(self, text="See Laser Tripwire Sensor History",
                            command= querylaser)
        sensorbutton3.pack()

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
class threatdetect:

    def __init__(self):
        self.sounddetected=0
        self.soundtime=0
        self.laserdetected=0
        self.lasertime=0
        self.motiondetected=0
        self.motiontime=0
        

    def determinethreat(self): #This method is the multithreading to run the methods all together
        f=threatdetect()
        soundthingspeak = Thread(target=f.read_sound_thingspeak)
        soundthingspeak.start()
        soundthingspeak.join()
        laserthingspeak = Thread(target=f.read_laser_thingspeak)
        laserthingspeak.start()
        laserthingspeak.join()
        motionthingspeak = Thread(target=f.read_motion_thingspeak)
        motionthingspeak.start()
        motionthingspeak.join()
        fullthreatlevel = Thread(target=f.threatlevel)
        fullthreatlevel.start()
        fullthreatlevel.join()
        app.after(5000,ah.determinethreat)
    def threatlevel(self):
        global CURRENT_STATUS
       
        '''The below code goes through all the possibilities for threat levels for sensors, it will compare the time that the sensor was tripped to the
            current time to determine if the sensor was recently tripped or if it just grabbed an old reading'''
    
        if self.laserdetected ==1 and self.sounddetected ==1 and self.motiondetected ==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <ONE_MINUTE:
               if (CURRENT_STATUS== "Threat level 3, all sensors tripped"):
                   return
               else:
                    CURRENT_STATUS= "Threat level 3, all sensors tripped"
                    ahh.popupError("Threat level 3")
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 3, all sensors tripped")
                    except:
                        print("sms failed to send")
                
       
    
        elif self.laserdetected == 1 and self.sounddetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <ONE_MINUTE:
                if(CURRENT_STATUS== "Threat level 2,laser has been broken and sound has been detected too please listen to most recent audio file"):
                    return
                else:
                    CURRENT_STATUS= "Threat level 2,laser has been broken and sound has been detected too please listen to most recent audio file"
                    ahh.popupError("Threat level 2, laser has been broken and sound has been detected")
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 2, laser has been broken and sound has been detected")
                    except:
                        print("sms failed to send")
        elif self.motiondetected == 1 and self.sounddetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds() <ONE_MINUTE:
                if(CURRENT_STATUS=="Threat level 2, motion has been detected and so has sound please listen to most recent audio file"):
                    return
                else:
                    CURRENT_STATUS="Threat level 2, motion has been detected and so has sound please listen to most recent audio file"
                    ahh.popupError("Threat level 2, motion and sound have been detected")
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 2, motion and sound have been detected")
                    except:
                        print("sms failed to send")
        elif self.motiondetected == 1 and self.laserdetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE:
                if( CURRENT_STATUS=="Threat level 2, motion has been detected and laser has been tripped"):
                    return
                else:
                    CURRENT_STATUS="Threat level 2, motion has been detected and laser has been tripped"
                    ahh.popupError("Threat level 2, motion has been detected and laser has been tripped")
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 2, motion has been detected and laser has been tripped")
                    except:
                        print("sms failed to send")
        elif self.sounddetected==1 and(datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.soundtime)).total_seconds()<ONE_MINUTE:
                if(CURRENT_STATUS=="Threat level 1, sound has been detected please listen to most recent audio file"):
                    return
                else:
                    CURRENT_STATUS="Threat level 1, sound has been detected please listen to most recent audio file"
                    ahh.popupError("Threat level 1, sound has been detected")
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 1, sound has been detected")
                    except:
                        print("sms failed to send")
            
        elif self.laserdetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.lasertime)).total_seconds() <ONE_MINUTE:
                if(CURRENT_STATUS=="Threat level 1, tripwire has been broken"):
                    return
                else:
                     CURRENT_STATUS="Threat level 1, tripwire has been broken"
                     ahh.popupError("Threat level 1, tripwire has been broken")
                     try:
                         client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 1, tripwire has been broken")
                     except:
                        print("sms failed to send")
            
        elif self.motiondetected==1 and (datetime.datetime.utcnow().replace(tzinfo=pytz.utc)-parser.parse(self.motiontime)).total_seconds() <ONE_MINUTE:
                if(CURRENT_STATUS=="Threat level 1, motion has been detected"):
                    return
                else:
                    CURRENT_STATUS="Threat level 1, motion has been detected"
                    ahh.popupError("Threat level 1, motion has been detected")
                    try:
                        client.messages.create(to="+16475295580", 
                           from_="+14158554536", 
                           body="Threat level 1, motion has been detected")
                    except:
                        print("sms failed to send")
        else:
               if(CURRENT_STATUS != "Safe"):
                   time.sleep(60)
                   CURRENT_STATUS = "Safe"
               else:
                   CURRENT_STATUS ="Safe"
                    
    
    def read_sound_thingspeak(self):
        '''The following code reads if the sound sensor has been triggered and stores that time in an array, it also stores the time
            it happened at in another array'''
        #global sounddetected
        #global soundtime
        db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db'
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        soundURL='https://api.thingspeak.com/channels/1152850/fields/1.json?api_keys='
        soundKEY='8T5J8V8E0LX16RY5'
        soundHEADER='&results=1' 
        sound_FULL=soundURL+soundKEY+soundHEADER
        soundresults=requests.get(sound_FULL).json()
        soundURL2='https://api.thingspeak.com/channels/1152850/fields/2.json?api_keys='
        soundKEY2='8T5J8V8E0LX16RY5'
        soundHEADER2='&results=1' 
        sound_FULL2=soundURL2+soundKEY2+soundHEADER2
        soundresults2=requests.get(sound_FULL2).json()
        data=[]
        try:
            for x in soundresults['feeds']:
                data.insert(0,int(x['field1']))
                self.sounddetected = data[0]
            for x in soundresults2['feeds']:
                data.insert(1,str(x['created_at']))
                self.soundtime=data[1]
        except:
            print("failed to read from SoundSensor Thingspeak")
        try:
            sql = "SELECT * FROM soundsensordata ORDER BY soundtime DESC LIMIT 1"
            recs = c.execute(sql)
            if True:
                for row in recs:
                 
                
                     if row != (1, self.soundtime):    
                            c.execute("""INSERT INTO soundsensordata VALUES(?,?)""",
                                    (self.sounddetected,self.soundtime))
                conn.commit() #commit needed
        except:
            ("Failed to insert into soundsensordata table")
        c.close()
    
    def read_laser_thingspeak(self):
        '''The following code reads if the laser tripwire sensor has been triggered and stores that time in an array, it also stores the time
        it happened at in another array'''
        #global self.laserdetected
        db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db'
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        laserKEY='QEAI32EFVL4ZM7ZR'
        laserURL= 'https://api.thingspeak.com/channels/1150122/fields/1.json?api_key='
        laserHEADER ='&results=1'
        laser_FULL = laserURL+laserKEY+laserHEADER
        laserresults=requests.get(laser_FULL).json()
        data2=[]
        try:
            for x in laserresults['feeds']:
                data2.insert(0,int(x['field1']))
                self.laserdetected = data2[0]
            for x in laserresults['feeds']:
                data2.insert(1,str(x['created_at']))
                self.lasertime=data2[1]
        except:
            print("failed to read from laser tripwire Thingspeak")
        try:
            sql = "SELECT * FROM lasersensordata ORDER BY lasertime DESC LIMIT 1"
            recs = c.execute(sql)
            if True:
                for row in recs:
                 
                     if row != (1, self.lasertime ):    
                            c.execute("""INSERT INTO lasersensordata VALUES(?,?)""",
                                  (self.laserdetected,self.lasertime))
                conn.commit() #commit needed
        except:
            print("failed to isnert into lasersensordata table")
        c.close()
    def read_motion_thingspeak(self):
        '''The following code reads if the motion sensor has been triggered and stores that time in an array, it also stores the time
        it happened at in another array'''
        #global motiondetected
        #global motiontime
        db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db'
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        motionURL='https://api.thingspeak.com/channels/1219425/fields/1.json?api_key='
        motionKEY='GQ6EDK3P60AS7YLO'
        motionHEADER='&results=1'
        motion_FULL=motionURL+motionKEY+motionHEADER
        motionresults=requests.get(motion_FULL).json()
        data3=[]
        try:
            for x in motionresults['feeds']:
                data3.insert(0,int(x['field1']))
                self.motiondetected=data3[0]
            for x in motionresults['feeds']:
                data3.insert(1,str(x['created_at']))
                self.motiontime=data3[1]
        except:
            print("failed to read from motion Thingspeak")
        try:
            sql = "SELECT * FROM motionsensordata ORDER BY motiontime DESC LIMIT 1"
            recs = c.execute(sql)
            if True:
                for row in recs:
                
                     if row != (1, self.motiontime ):
                            c.execute("""INSERT INTO motionsensordata VALUES(?,?)""",
                                  (self.motiondetected,self.motiontime))
                conn.commit() #commit needed
        except:
            print("failed to insert into motionsensordata table")
        c.close()
ahh=SecurityPage
ah=threatdetect()
app = AlphaSecurity()
app.title("Security System Control Console")
app.after(5000,ah.determinethreat)
app.mainloop()
