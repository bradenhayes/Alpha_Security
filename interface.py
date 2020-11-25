import tkinter as tk
from tkinter import *
import sqlite3
import os
import dropbox

LARGE_FONT= ("Verdana", 12)
substatus=1

class AlphaSecurity(tk.Tk):

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

        
class StartPage(tk.Frame):
    

    def __init__(self, parent, controller):
        def close():
            controller.destroy()
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Alpha Security", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        security = tk.Button(self,
                      text ="Security Status",
                      command = lambda: controller.show_frame(SecurityPage))
        
        subscription = tk.Button(self,
                      text ="Subscription",
                      command = lambda: controller.show_frame(PreSubscriptionPage))
        videostream = tk.Button(self,
                   text="Video Stream",
                   fg="blue",
                   command = lambda: controller.show_frame(VideoPage))
        audiofiles = tk.Button(self,
                   text="Audio Files",
                   fg="blue",
                   command = lambda: controller.show_frame(AudioPage))
        sensorhistory = tk.Button(self,
                   text="Sensor History",
                   fg="blue",
                   command = lambda: controller.show_frame(SensorPage))
        quitbutton = tk.Button(self,
                   text="QUIT",
                   fg="red",
                   command = close)


        security.pack()
        subscription.pack()

        videostream.pack()
        audiofiles.pack()
        sensorhistory.pack()
        quitbutton.pack()
class CameraStartpage(tk.Frame):
    

    def __init__(self, parent, controller):
        def close():
            controller.destroy()
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

class SecurityPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Security Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
class PreSubscriptionPage(tk.Frame):
    
    def __init__(self, parent, controller):
        global substatus
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Would you like to...", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        UpgradeButton = tk.Button(self, text="Upgrade Package",
                            command=lambda: controller.show_frame(SubscriptionPage))
        UpgradeButton.pack()
          
        
        DowngradeButton = tk.Button(self, text="Downgrade Package",
                            command=lambda: controller.show_frame(SubscriptionPage))
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
        '''cameracheck=tk.Checkbutton(self,text="Camera package",variable=self.cameravar,command=self.callback)
        cameracheck.pack()
        soundcheck=tk.Checkbutton(self,text="Sound Security Package",variable=self.soundvar,command=self.callback)
        soundcheck.pack()
        motioncheck=tk.Checkbutton(self,text="Motion Detection Package",variable=self.motionvar,command=self.callback)
        motioncheck.pack()
        lasercheck=tk.Checkbutton(self,text="Laser Tripwire Package",variable=self.laservar,command=self.callback)
        lasercheck.pack()'''
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
        
        
        
    
    '''def callback(self):
        if self.soundvar.get()==1 and self.cameravar.get()==1 and self.motionvar.get()==1:
            
            ConfirmButton=tk.Button(self, text="Confirm",
                                command=lambda: self.controller.show_frame(SecurityPage))
            ConfirmButton.pack()
            
    def callback1(self):
        if self.soundvar.get()==1:
            ConfirmButton=tk.Button(self, text="Confirm",
                                command=lambda: self.controller.show_frame(SecurityPage))
            ConfirmButton.destroy()
    def callback2(self):
        if self.motionvar.get()==1:
            ConfirmButton=tk.Button(self, text="Confirm",
                                command=lambda: self.controller.show_frame(SecurityPage))
            ConfirmButton.destroy()    
    def callback3(self):
        if self.laservar.get()==1:
            ConfirmButton=tk.Button(self, text="Confirm",
                                command=lambda: self.controller.show_frame(SecurityPage))
            ConfirmButton.pack()    
  
       ''' 
            

class VideoPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Video Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
class AudioPage(tk.Frame):

    def __init__(self, parent, controller):
        
            
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Audio Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        def audioOpen():
            dbx = dropbox.Dropbox('8WNB4VteJFUAAAAAAAAAAQkkCfn_aeDYNxNuE2p8sIRNh5fWyWuZhLSqwXT5UZ2p')
            entries = dbx.files_list_folder('').entries

            for entry in entries:
                if isinstance(entry, dropbox.files.FileMetadata):  # this entry is a file
                    metadata,f = dbx.files_download(entry.path_lower)
                    out=open(entry.name,'wb')
                    out.write(f.content)
            
            controller.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("mp3 files",".mp3"),("all files",".*")))
        audiobutton = tk.Button(self, text="Search Directory",
                            command= audioOpen)
        audiobutton.pack()
       
        
        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
class SensorPage(tk.Frame):

    def __init__(self, parent, controller):
        def query():
            dbconnect = sqlite3.connect('sensordata.db');
            cursor = dbconnect.cursor(); #create cursor
            cursor.execute('SELECT * FROM sensors');
            dbconnect.close();
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sensor Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        
        sensorbutton = tk.Button(self, text="See Sensor History",
                            command= query,
                                 width = 25,
                                 height = 5)
        sensorbutton.pack()

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

app = AlphaSecurity()
app.mainloop()
