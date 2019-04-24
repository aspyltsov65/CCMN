import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import requests
import urllib3


urllib3.disable_warnings()
username = 'RO'
password = 'just4reading'
hostname = 'https://cisco-cmx.unit.ua/'
query_active = 'api/location/v2/clients/'


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.iconbitmap('@python.xbm')
        tk.Tk.wm_title(self, "CCMN")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.add_img1 = tk.PhotoImage(file='dashboard_button.gif')
        self.add_img2 = tk.PhotoImage(file='map_button.gif')
        self.add_img3 = tk.PhotoImage(file='presense_button.gif')

        self.frames = {}
        for F in (StartPage, Map, Presense):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(StartPage)
        globals()
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

        button1 = tk.Button(bottomframe, bd=0, state=DISABLED,compound=tk.TOP, image=controller.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, command=lambda:
        controller.show_frame(Map), bd=0, compound=tk.TOP, image=controller.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, command=lambda:
        controller.show_frame(Presense), bd=0, compound=tk.TOP, image=controller.add_img3)
        button3.pack(side=tk.LEFT)


class Map(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["bg"] = "white"
        bottomframe = tk.Frame(self, parent)
        bottomframe["bg"] = '#3c8081'
        bottomframe.pack(side=tk.TOP, fill=tk.X)

        button1 = tk.Button(bottomframe, command=lambda:
        (controller.show_frame(StartPage)), bd=0, compound=tk.TOP, image=controller.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, bd=0, state=DISABLED, compound=tk.TOP, image=controller.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, command=lambda:
        controller.show_frame(Presense), bd=0, compound=tk.TOP, image=controller.add_img3)
        button3.pack(side=tk.LEFT)

        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.verify = False

        self.img = plt.imread("Perks/e1.png")
        self.leftpanel = tk.Frame(self, parent)
        self.leftpanel["bg"] = 'white'
        self.leftpanel.pack(side=LEFT, fill=tk.Y)
        self.ment = StringVar()
        self.leftpanel_switch = tk.Frame(self.leftpanel)
        self.leftpanel_switch.pack(side=TOP)

        self.floor_switch = 1

        self.button_s_1 = tk.Button(self.leftpanel_switch, state=NORMAL, command=lambda:
        floor_switch(self, 1), text='Floor 1', bd=0, compound=tk.TOP)
        self.button_s_1.pack(side=LEFT)
        self.button_s_2 = tk.Button(self.leftpanel_switch, state=NORMAL, command=lambda:
        floor_switch(self, 2), text='Floor 2', bd=0, compound=tk.TOP)
        self.button_s_3 = tk.Button(self.leftpanel_switch, state=NORMAL, command=lambda:
        refresh(self), text='Refresh', bd=0, compound=tk.TOP)
        self.button_s_3.pack(side=RIGHT)
        self.button_s_2.pack(side=RIGHT)

        label = Label(self.leftpanel, text='Type MacAddress or UserName', bd=0, compound=tk.TOP)
        label.pack(side=TOP)

        self.mEntry = Entry(self.leftpanel, textvariable=self.ment)
        self.mEntry.pack(side=TOP, fill=tk.X)
        self.scrollbar = Scrollbar(self.leftpanel, orient=VERTICAL)
        self.listbox = Listbox(self.leftpanel, width=50, height=20, yscrollcommand=self.scrollbar.set)
        self.scrollbar = tk.Scrollbar(self.listbox, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")
        self.scrollbar.config(command=self.listbox.yview)
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.connected = ""
        self.info_label = Label(self)
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.f, self)
        self.cur_selection = None

    def parse(self):
        globals()
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.imshow(self.img, extent=[0, 1550, 770, 0])
        data = self.session.get(hostname + query_active).json()
        list = Listbox(self.leftpanel, bd=2, bg='#9DBFC0', width=27,
            font="Helvetica 16 bold italic", fg = "#3c8081")
        info_label = Label(self, justify=LEFT, font="Arial 16", fg="#bc5151")
        typed_text = self.ment.get()

        for mac in data:
            if self.listbox.curselection() and (mac['macAddress'] in str(self.listbox.get((self.listbox.curselection())))
                        or (mac['userName'] in str(self.listbox.get(self.listbox.curselection())) and mac['userName'])):
                self.a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=8)
                self.a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'], fontsize=8)
                list.insert(END, mac['macAddress'] + ' \t' + mac['userName'])
                label_paste(info_label, mac)
            elif str(self.floor_switch) in mac['mapInfo']['mapHierarchyString'] and mac['ipAddress']:
                if self.ment and (typed_text in mac['macAddress'] or typed_text in mac['userName']):
                    list.insert(END, mac['macAddress'] + ' \t' + mac['userName'])
                elif not self.ment:
                    list.insert(END, mac['macAddress'] + ' \t' + mac['userName'])
                if not self.listbox.curselection():
                    self.a.plot(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], 'ro', markersize=8)
                    self.a.text(mac['mapCoordinate']['x'], mac['mapCoordinate']['y'], mac['userName'], fontsize=8)
            if not mac['macAddress'] in self.connected and mac['ipAddress']:
                self.connected += mac['macAddress']
                if " " in self.connected and '1' in mac['mapInfo']['mapHierarchyString']:
                    messagebox.showinfo("Notification", mac['macAddress'] + " " + mac['userName'] + " now is on the first floor")
                elif " " in self.connected:
                    messagebox.showinfo("Notification", mac['macAddress'] + " " + mac['userName'] + "now is on the second floor")
        self.connected += " "

        if (self.listbox.curselection()):
            list.selection_set(self.listbox.curselection())

        if list:
            self.listbox.pack_forget()
            self.listbox = list
            if (list.curselection()):
                self.listbox.selection_set(list.curselection())
            self.listbox.pack(side=LEFT, fill=Y)
        if self.cur_selection != self.listbox.curselection():
            self.cur_selection = self.listbox.curselection()
            self.canvas._tkcanvas.pack_forget()
            self.canvas = FigureCanvasTkAgg(self.f, self)
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        if not self.listbox.curselection():
            self.info_label.pack_forget()


class Presense(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["bg"] = "#56b8b9"
        bottomframe = tk.Frame(self, parent)
        bottomframe["bg"] = '#3c8081'
        bottomframe.pack(side=tk.TOP, fill=tk.X)
        button1 = tk.Button(bottomframe, command=lambda:
        controller.show_frame(StartPage), bd=0, compound=tk.TOP, image=controller.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, command=lambda:
        controller.show_frame(Map), bd=0, compound=tk.TOP, image=controller.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, bd=0,state=DISABLED, compound=tk.TOP, image=controller.add_img3)
        button3.pack(side=tk.LEFT)


def close_window():
  global running
  running = False
  app.destroy()


def label_paste(info_label, mac):
    info_label['text'] = "\n\n\n\nMacAddress:\t\t " + mac['macAddress'] + "\nFloor:\t\t\t "
    if '1st_Floor' in mac['mapInfo']['mapHierarchyString']:
        info_label['text'] += "1st_Floor"
    else:
        info_label['text'] += "2nd_Floor"
    info_label['text'] += "\nRSSI:\t\t\t " + \
        str(mac['statistics']['maxDetectedRssi']['rssi']) + "\nSSID:\t\t\t " + \
        mac['ssId'] + "\nDevice type:\t\t " + str(mac['manufacturer']) + \
        "\nUserName:\t\t " + mac['userName'] + "\nFirst Located Time:\t " + \
        mac['statistics']['firstLocatedTime'] + "\nLast Located Time:\t\t " + \
        mac['statistics']['lastLocatedTime']


def floor_switch(self, cont):
    if cont == 1:
        self.img = plt.imread("Perks/e1.png")
    else:
        self.img = plt.imread("Perks/e2.png")
    self.floor_switch = cont
    if self.listbox.curselection():
        self.listbox.selection_clear(self.listbox.curselection())
    self.sum = 0
    refresh(self)


def refresh(self):
    self.cur_selection = None


running = TRUE

app = SeaofBTCapp()
app.geometry("1600x1200+500+100")
app.protocol("WM_DELETE_WINDOW", close_window)
app.bind('<Escape>', lambda e: close_window())

mapi = app.frames[Map]
mapi.parse()

while running:
    mapi.parse()
    app.update()
