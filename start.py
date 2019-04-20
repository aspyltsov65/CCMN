import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from tkinter import *
import requests
import json
import urllib3
urllib3.disable_warnings()

username = 'RO'
password = 'just4reading'
hostname = 'https://cisco-cmx.unit.ua/'
query_mac = 'api/location/v1/history/clients/'
query_active = 'api/location/v2/clients/'
query_allhistory = 'api/location/v1/history/clients'
mac_ad = '00%3A03%3Aac%3A33%3A94%3A0e'

LARGE_FONT= ("Verdana", 12)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)

        #tk.Tk.iconbitmap(self, default="clienticon.ico")
        self.iconbitmap('@python.xbm')
        tk.Tk.wm_title(self, "CCMN")


        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Map, Presense):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        self["bg"] = "#56b8b9"
        bottomframe = tk.Frame(self,parent)
        bottomframe["bg"] = '#3c8081'
        bottomframe.pack(side=tk.TOP, fill=tk.X)
        self.add_img2 = tk.PhotoImage(file='map_button.gif')
        self.add_img3 = tk.PhotoImage(file='presense_button.gif')
        self.add_img1 = tk.PhotoImage(file='dashboard_button.gif')
        button1 = tk.Button(bottomframe, bd=0, state=DISABLED,compound=tk.TOP, image=self.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, command=lambda: controller.show_frame(Map), bd=0,
                            compound=tk.TOP, image=self.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, command=lambda: controller.show_frame(Presense), bd=0,
                            compound=tk.TOP, image=self.add_img3)
        button3.pack(side=tk.LEFT)


class Map(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["bg"] = "#56b8b9"
        bottomframe = tk.Frame(self, parent)
        bottomframe["bg"] = '#3c8081'
        bottomframe.pack(side=tk.TOP, fill=tk.X)
        self.add_img2 = tk.PhotoImage(file='map_button.gif')
        self.add_img3 = tk.PhotoImage(file='presense_button.gif')
        self.add_img1 = tk.PhotoImage(file='dashboard_button.gif')
        button1 = tk.Button(bottomframe, command=lambda: (controller.show_frame(StartPage), controller.show_frame(Map)), bd=0,
                            compound=tk.TOP, image=self.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, bd=0, state=DISABLED, compound=tk.TOP, image=self.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, command=lambda: controller.show_frame(Presense), bd=0,
                            compound=tk.TOP, image=self.add_img3)
        button3.pack(side=tk.LEFT)

        img = plt.imread("Perks/e1.png")
        f = Figure(figsize=(5, 5), dpi=100)
        a = f.add_subplot(111)
        a.imshow(img, extent=[0, 1550, 770, 0])

        session = requests.Session()
        session.verify = False
        session.auth = (username, password)
        auth = session.post(hostname)

        response = session.get(hostname + query_active)
        data = response.text
        data = json.loads(data)
        for mac in data:
            # if mac['ipAddress']:
                a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=8)
                a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'], fontsize=8)
        canvas = FigureCanvasTkAgg(f, self)
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class Presense(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["bg"] = "#56b8b9"
        bottomframe = tk.Frame(self, parent)
        bottomframe["bg"] = '#3c8081'
        bottomframe.pack(side=tk.TOP, fill=tk.X)
        self.add_img2 = tk.PhotoImage(file='map_button.gif')
        self.add_img3 = tk.PhotoImage(file='presense_button.gif')
        self.add_img1 = tk.PhotoImage(file='dashboard_button.gif')
        button1 = tk.Button(bottomframe, command=lambda: controller.show_frame(StartPage), bd=0,
                            compound=tk.TOP, image=self.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, command=lambda: controller.show_frame(Map), bd=0,
                            compound=tk.TOP, image=self.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, bd=0,state=DISABLED, compound=tk.TOP, image=self.add_img3)
        button3.pack(side=tk.LEFT)


class PageThree(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
        label.pack(pady=10,padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        f = Figure(figsize=(5,5), dpi=100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])



        canvas = FigureCanvasTkAgg(f, self)
        #canvas.show()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)



app = SeaofBTCapp()
plt.show(block=False)
app.geometry("1600x1200+500+100")
app.mainloop()
