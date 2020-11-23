import tkinter as tk


LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, SecurityPage, SubscriptionPage, VideoPage, AudioPage, SensorPage):

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
                      command = lambda: controller.show_frame(SubscriptionPage))
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

class SecurityPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Security Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class SubscriptionPage(tk.Frame):
import tkinter as tk


LARGE_FONT= ("Verdana", 12)


class AlphaSecurity(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, SecurityPage, SubscriptionPage, VideoPage, AudioPage, SensorPage):

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
                      command = lambda: controller.show_frame(SubscriptionPage))
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

class SecurityPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Security Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

class SubscriptionPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Subscription Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()



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

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()
        
class SensorPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Sensor Page", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = tk.Button(self, text="Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

app = AlphaSecurity()
app.mainloop()


