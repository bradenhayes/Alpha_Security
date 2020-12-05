import tkinter as tk
from tkinter import *
from tkinter import Tk, BOTH, messagebox
import sqlite3
import os
import dropbox
import webbrowser
import pygame
from pydub import AudioSegment
from pydub.playback import play
"hehe"
LARGE_FONT= ("Verdana", 12)
class AlphaSecurity(tk.Tk): #creating inital window

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage,CameraStartpage, SecurityPage,PreSubscriptionPage, SubscriptionPage, VideoPage, AudioPage, SensorPage):

            frame = F(container, self)

            self.frames[F] = frame
            
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()

        
class StartPage(tk.Frame): #creates the start page every user will start with
    

    def __init__(self, parent, controller):
        def close(): # creates close button that will be implimend in the quit button
            controller.destroy() #this will destroy the window ending the program
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Alpha Security", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        security = tk.Button(self,
                      text ="Security Status",
                      command = lambda: controller.show_frame(SecurityPage)) #security button that when selected will go to security page
        
        subscription = tk.Button(self,
                      text ="Subscription",
                      command = lambda: controller.show_frame(PreSubscriptionPage))  #subscription button that when selected will go to subscription page
        videostream = tk.Button(self,
                   text="Video Stream",
                   fg="blue",
                   command = lambda: controller.show_frame(VideoPage))  #Video button that when selected will go to video page
        audiofiles = tk.Button(self,
                   text="Audio Files",
                   fg="blue",
                   command = lambda: controller.show_frame(AudioPage))  #Audio files button that when selected will go to Audio file page
        sensorhistory = tk.Button(self,
                   text="Sensor History",
                   fg="blue",
                   command = lambda: controller.show_frame(SensorPage))  #sensor history button that when selected will go to sensor history page
        quitbutton = tk.Button(self,
                   text="QUIT",
                   fg="red",
                   command = close) #Will terminiate window when clicked


        security.pack()
        subscription.pack()

        videostream.pack()
        audiofiles.pack()
        sensorhistory.pack()
        quitbutton.pack() # packs all buttons made above
class CameraStartpage(tk.Frame): #if only subscriped to camera this is now the main page
    

    def __init__(self, parent, controller):
        def close():
            controller.destroy() #creates destroy button
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Alpha Security", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        subscription = tk.Button(self,
                      text ="Subscription",
                      command = lambda: controller.show_frame(PreSubscriptionPage))
        videostream = tk.Button(self,
                   text="Video Stream",
                   fg="blue",
                   command = lambda: controller.show_frame(VideoPage))
        subscription.pack()
        videostream.pack()

class SecurityPage(tk.Frame):#used to determine the level of threat among the security system

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Security Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
class PreSubscriptionPage(tk.Frame): # allows the user to either upgrade or downgrade there system
    
    def __init__(self, parent, controller):
        global substatus
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Would you like to...", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        UpgradeButton = tk.Button(self, text="Upgrade Package",
                            command=lambda: controller.show_frame(SubscriptionPage)) #takes user to subscription page and shows packages
        UpgradeButton.pack()
          
        
        DowngradeButton = tk.Button(self, text="Downgrade Package",
                            command=lambda: controller.show_frame(SubscriptionPage)) #takes user to subscription page and shows packages
        DowngradeButton.pack()
         
class SubscriptionPage(tk.Frame):

    def __init__(self, parent, controller):
    
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Subscription Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
    
        self.controller=controller
        self.cameravar=IntVar()
        self.soundvar=IntVar()
        self.motionvar=IntVar()
        self.laservar=IntVar()
        self.varr=IntVar()
        fullbutt=Radiobutton(self,text="Complete Package (Tripwire, Sound security, Motion detection and camera)",variable=self.varr,value=0,command= self.callbackfull)
        halfbutt=Radiobutton(self,text="Camera Package",variable=self.varr,value=1,command= self.callbackcamera)
        fullbutt.pack()
        halfbutt.pack()
        button1 = tk.Button(self, text="Home",
                            command=lambda: self.controller.show_frame(StartPage))
        button1.pack()
    def callbackfull(self):
        self.UpgradeButton=tk.Button(self, text="Click here to confirm upgrade of package",
                                command=lambda: self.controller.show_frame(StartPage))
   
        self.UpgradeButton.pack()
    

    def callbackcamera(self):
        self.DowngradeButton=tk.Button(self, text="Click here to confirm downgrade of package",
                                command=lambda: self.controller.show_frame(CameraStartpage))
        self.DowngradeButton.pack()
        
        


class VideoPage(tk.Frame):

    def __init__(self, parent, controller):
        def Stream(): #will allow the button to open an external link with the video stream
            webbrowser.open_new(r"index.html")
            
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Launch Stream", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        link = tk.Button(self, text="Video Stream",
                            command= Stream) #launches stream in browser
        link.pack() #packs button

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage)) #will take the user back to startpage
        button1.pack()
        
class AudioPage(tk.Frame):

    def __init__(self, parent, controller):
            
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Audio Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        def audioOpen(): #downloading the most recent files from dropbox to then be depolyed
            global check
            pygame.mixer.init()
          
            dbx = dropbox.Dropbox('8WNB4VteJFUAAAAAAAAAAQkkCfn_aeDYNxNuE2p8sIRNh5fWyWuZhLSqwXT5UZ2p')#dropbox access code
            entries = dbx.files_list_folder('').entries

            for entry in entries:
                if isinstance(entry, dropbox.files.FileMetadata):  # this entry is a file
                    metadata,f = dbx.files_download(entry.path_lower)
                    out=open(entry.name,'wb')
                    out.write(f.content)
            for root, dirs, files in(os.walk("/home/pi/Desktop/Sysc3010/Project/AudioFiles")): #downloading the files to specific location to be accessed later
                    files.sort()
                    for file in files:
                        if file.endswith(".mp3"): #ends file name with .mp3 to be played later
                            f = open(os.path.join(root,file),'rb')
                            filebutton = tk.Button(self, text=os.path.basename(f.name),
                                command=lambda file=file: play_audio(file))
                            filebutton.pack()
        def play_audio(file):
            global check
            messagebox.showinfo("Button label", file)
            recording= AudioSegment.from_file('/home/pi/Desktop/Sysc3010/Project/AudioFiles/' + str(file))#uses the location to now access files
            loud_recording = recording +500
            play(loud_recording)#plays recording
            #pygame.mixer.music.load(loud_recording)
            #pygame.mixer.music.play(loops=0)
            
            
            
        audiobutton = tk.Button(self, text="Search Directory",
                            command=audioOpen) #calls the function above to download then search the files
        audiobutton.pack()
       
        
        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))#goes back to homepage
        button1.pack()
        
class SensorPage(tk.Frame):

    def __init__(self, parent, controller):
        def querymotion(verbose=True): #establishing a connection between the database and the table of motion
            db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db' #accessing the data base    
            conn = sqlite3.connect(db_path) #connection
            c = conn.cursor()
            sql = "SELECT * FROM motionsensordata" #selecting the motion sensor table
            recs = c.execute(sql)
            showdata="" #shows the data in table
            if verbose:
                for row in recs:
                    showdata+=str(row)+ "\n"
            messagebox.showinfo(title="Sound Sensor History",message=showdata)    
            c.close() #closes connection to be re-esablished later
        def querysound(verbose=True): #establishing a connection between the database and the table of sound
            db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db'  #accessing the data base
            conn = sqlite3.connect(db_path) #connection
            c = conn.cursor()
            sql = "SELECT * FROM soundsensordata"#selecting the sound sensor table
            recs = c.execute(sql)
            showdata=""#shows the data
            if verbose:
                for row in recs:
                    showdata+=str(row)+ "\n"
            messagebox.showinfo(title="Sound Sensor History",message=showdata)        
            c.close()#closes connection to be re-esablished later
        def querylaser(verbose=True):#establishing a connection between the database and the table of laser
            db_path = '/home/pi/Desktop/Sysc3010/Project/sensordata.db' #accessing the data base
            conn = sqlite3.connect(db_path)#connection established
            c = conn.cursor()
            sql = "SELECT * FROM lasersensordata"#selecting the laser sensor table
            recs = c.execute(sql)
            showdata=''#shows data
            if verbose:
                for row in recs:
                    showdata+=str(row)+ "\n"
            messagebox.showinfo(title="Laser Tripwire Sensor History",message=showdata)
            c.close()#closes connection to be re-esablished later
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sensor Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        sensorbutton = tk.Button(self, text="See Motion Sensor History",
                            command= querymotion)#opens Motion Sensor history using the databases
                            
        sensorbutton.pack()
        sensorbutton2 = tk.Button(self, text="See Sound Sensor History",
                            command= querysound)#opens Tripwires sensor history using the databases
        sensorbutton2.pack()
        sensorbutton3 = tk.Button(self, text="See Laser Tripwire Sensor History",
                            command= querylaser)#opens Sound Sensor history using the databases
        sensorbutton3.pack()

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage)) #allows user to go back to the start page
        button1.pack()

app = AlphaSecurity() #runs programs
app.mainloop() #at the end to ensure everything is encaplsued in the loop
