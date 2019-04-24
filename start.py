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
import time
import urllib3
import threading
urllib3.disable_warnings()


def floor_switch(self, cont):
    if cont == 1:
        self.img = plt.imread("Perks/e1.png")
    else:
        self.img = plt.imread("Perks/e2.png")
    self.floor_switch = cont
    if (self.listbox.curselection()):
        self.listbox.selection_clear(self.listbox.curselection())
    self.sum = 0


class SeaofBTCapp(tk.Tk):

    frames = {}

    def __init__(self):
        super().__init__()
        self.img1 = tk.PhotoImage(file='dashboard_button.gif')
        self.img2 = tk.PhotoImage(file='map_button.gif')
        self.img3 = tk.PhotoImage(file='presense_button.gif')

    def create_tabs(self):
        top_tabs = tk.Frame(self)
        top_tabs.pack(side="top", fill="both", expand=True)
        top_tabs.grid_rowconfigure(0, weight=1)
        top_tabs.grid_columnconfigure(0, weight=1)

        for F in (StartPage, Map, Presense):
            frame = F(top_tabs, self)
            frame.create_button_frame(self, top_tabs)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)

    def show_frame(self, tab):
        frame = self.frames[tab]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, container, *args, **kwargs):
        tk.Frame.__init__(self, container)

    def create_button_frame(self, window, container):

        button_frame = tk.Frame(container)
        button_frame['bg'] = '#3c8081'
        button_frame.pack(side=tk.TOP, fill=tk.X)

        button1 = tk.Button(button_frame, state=DISABLED,
                            compound=tk.TOP, image=window.img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(button_frame, command=lambda: window.show_frame(StartPage),
                            compound=tk.TOP, image=window.img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(button_frame, command=lambda: window.show_frame(Presense), compound=tk.TOP, image=window.img3)
        button3.pack(side=tk.LEFT)


class Map(tk.Frame):
    def __init__(self, parent, controller, *args, **kwargs):
        tk.Frame.__init__(self, controller)

        self.img = plt.imread("Perks/e1.png")

        self.sum = 0
        self.leftpanel = tk.Frame(self, parent)
        self.leftpanel["bg"] = 'white'
        self.leftpanel.pack(side=LEFT, fill=tk.Y)

        self.ment = StringVar()

        self.leftpanel_switch = tk.Frame(self.leftpanel)
        self.leftpanel_switch.pack(side=TOP)

        self.floor_switch = 1

        self.button_s_1 = tk.Button(self.leftpanel_switch, state=NORMAL, command=lambda: floor_switch(self, 1), text='Floor 1', bd=0,
                            compound=tk.TOP)
        self.button_s_1.pack(side=LEFT)

        self.button_s_2 = tk.Button(self.leftpanel_switch, state=NORMAL, command=lambda: floor_switch(self, 2), text='Floor 2', bd=0,
                            compound=tk.TOP)
        self.button_s_2.pack(side=RIGHT)

        label = Label(self.leftpanel, text='Type MacAddress or UserName', bd = 0, compound = tk.TOP)
        label.pack(side=TOP)

        self.mEntry = Entry(self.leftpanel, textvariable=self.ment)
        self.mEntry.pack(side=TOP, fill=tk.X)
        self.listbox = Listbox(self.leftpanel, width=50, height=20)
        self.scrollbar = tk.Scrollbar(self.listbox, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")

        self.f = Figure(figsize=(5, 5), dpi=100)
        self.rsum = 0
        self.canvas = FigureCanvasTkAgg(self.f, self)

    def set_switch(self, cont):
        self.floor_switch = cont

    def create_button_frame(self, window, container):

        button_frame = tk.Frame(container)
        button_frame['bg'] = '#3c8081'
        button_frame.pack(side=tk.TOP, fill=tk.X)

        button1 = tk.Button(button_frame, command=lambda: window.show_frame(StartPage),
                            compound=tk.TOP, image=window.img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(button_frame,  state=DISABLED, compound=tk.TOP, image=window.img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(button_frame, command= lambda: (window.show_frame(Presense)), compound=tk.TOP, image=window.img3)
        button3.pack(side=tk.LEFT)

    def parse(self):
        globals()
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)
        # print("~~~~~~~{}".format(type(self.a)))

        self.a.imshow(self.img, extent=[0, 1550, 770, 0])

        data = ApiProcess.login()

        list = Listbox(self.leftpanel, bd=2, bg='#9DBFC0', width=27, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=list.yview)
        i = 0
        r = 0
        if self.listbox.curselection():
            sel = str(self.listbox.get((self.listbox.curselection())))
        if self.listbox.curselection():
            for mac in data:
                if mac['ipAddress']:
                    if int(sel.find(mac['macAddress'])) > -1 or int(sel.find(mac['userName']) > -1):
                        if (int(sel.find(mac['userName']) > -1 and int(sel.find(mac['macAddress'])) == -1 and not mac['userName'])):
                            continue
                        self.a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=8)
                        self.a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'], fontsize=8)
                        r += mac['mapCoordinate']['x'] + mac['mapCoordinate']['y']
                        break
        typed_text = self.ment.get()
        for mac in data:
            if mac['ipAddress']:
                if self.floor_switch == 1 and int(mac['mapInfo']['mapHierarchyString'].find('1st_Floor')) > -1:
                    if self.ment:
                        if int(mac['macAddress'].find(typed_text)) == 0 or int(mac['userName'].find(typed_text)) == 0:
                            if not self.listbox.curselection():
                                self.a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=8)
                                self.a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'],
                                         fontsize=8)
                            list.insert(END, mac['macAddress'] + ' \t' + mac['userName'])
                            i += mac['mapCoordinate']['x'] + mac['mapCoordinate']['y']
                    else:
                        if not self.listbox.curselection():
                            self.a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=8)
                            self.a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'], fontsize=8)
                        list.insert(END, mac['macAddress'] + ' \t' + mac['userName'])
                        i += mac['mapCoordinate']['x'] + mac['mapCoordinate']['y']
                elif self.floor_switch == 2 and int(mac['mapInfo']['mapHierarchyString'].find('2nd_Floor')) > -1:
                    if self.ment:
                        if int(mac['macAddress'].find(typed_text)) == 0 or int(mac['userName'].find(typed_text)) == 0:
                            if not self.listbox.curselection():
                                self.a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=8)
                                self.a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'],
                                         fontsize=8)
                            list.insert(END, mac['macAddress'] + ' \t' + mac['userName'])
                            i += mac['mapCoordinate']['x'] + mac['mapCoordinate']['y']
                    else:
                        if not self.listbox.curselection():
                            self.a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=8)
                            self.a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'], fontsize=8)
                        list.insert(END, mac['macAddress'] + ' \t' + mac['userName'])
                        i += mac['mapCoordinate']['x'] + mac['mapCoordinate']['y']
        cur = self.mEntry.index(INSERT)
        if r != self.rsum and self.listbox.curselection():
            self.rsum = r
            if (self.listbox.curselection()):
                list.selection_set(self.listbox.curselection())
            if list:
                self.listbox.pack_forget()
                self.listbox = list
                if (list.curselection()):
                    self.listbox.selection_set(list.curselection())
                self.listbox.pack(side=LEFT, fill=Y)

            self.canvas._tkcanvas.pack_forget()
            self.canvas = FigureCanvasTkAgg(self.f, self)
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        if i != self.sum :
            self.sum = i
            # if r:

            # ba = self.listbox.get()
            if (self.listbox.curselection()):
                list.selection_set(self.listbox.curselection())
            if list:
                self.listbox.pack_forget()
                self.listbox = list
                if (list.curselection()):
                    self.listbox.selection_set(list.curselection())
                self.listbox.pack(side=LEFT, fill=Y)
            self.canvas._tkcanvas.pack_forget()
            self.canvas = FigureCanvasTkAgg(self.f, self)
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.mEntry.icursor(cur)


class Presense(tk.Frame):

    bg = "#56b8b9"

    def __init__(self, container, *args, **kwargs):
        tk.Frame.__init__(self, container)

    def create_button_frame(self, window, container):

        button_frame = tk.Frame(container)
        button_frame['bg'] = '#3c8081'
        button_frame.pack(side=tk.TOP, fill=tk.X)

        button1 = tk.Button(button_frame, command=lambda: window.show_frame(StartPage),
                            compound=tk.TOP, image=window.img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(button_frame, command=lambda: window.show_frame(StartPage),
                            compound=tk.TOP, image=window.img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(button_frame, state=DISABLED, compound=tk.TOP, image=window.img3)
        button3.pack(side=tk.LEFT)


class ApiProcess():

    username = 'RO'
    password = 'just4reading'
    hostname = 'https://cisco-cmx.unit.ua/'
    query_mac = 'api/location/v1/history/clients/'
    query_active = 'api/location/v2/clients/'
    query_all_history = 'api/location/v1/history/clients'
    mac_ad = ''

    @classmethod
    def login(cls):
        """Login to cisco-cmx.unit.ua, create request, get data from API"""
        session = requests.Session()
        session.auth = (cls.username, cls.password)
        session.verify = False
        response = session.get(cls.hostname + cls.query_active)
        return response.json()


def close_window():
    global running
    running = False
    app.destroy()


if __name__ == "__main__":

    running = TRUE

    app = SeaofBTCapp()
    app.create_tabs()
    app.show_frame(StartPage)

    app.geometry("1600x1200+500+100")
    app.title("CCMN")
    app.protocol("WM_DELETE_WINDOW", close_window)
    app.bind('<Escape>', lambda e: close_window())

    mapi = app.frames[Map]
    mapi.parse()

    while running:
        mapi.parse()
        app.update()
