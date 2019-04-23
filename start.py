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

username = 'RO'
password = 'just4reading'
hostname = 'https://cisco-cmx.unit.ua/'
query_mac = 'api/location/v1/history/clients/'
query_active = 'api/location/v2/clients/'
query_allhistory = 'api/location/v1/history/clients'
mac_ad = ''


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):

        tk.Tk.__init__(self, *args, **kwargs)


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


def floor_switch(self, cont):
    if cont == 1:
        self.img = plt.imread("Perks/e1.png")
    else:
        self.img = plt.imread("Perks/e2.png")
    self.floor_switch = cont
    self.listbox.selection_clear(self.listbox.curselection())
    self.sum = 0

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
    def set_switch(self, cont):
        self.floor_switch = cont
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["bg"] = "white"
        bottomframe = tk.Frame(self, parent)
        bottomframe["bg"] = '#3c8081'
        bottomframe.pack(side=tk.TOP, fill=tk.X)
        self.add_img2 = tk.PhotoImage(file='map_button.gif')
        self.add_img3 = tk.PhotoImage(file='presense_button.gif')
        self.add_img1 = tk.PhotoImage(file='dashboard_button.gif')
        button1 = tk.Button(bottomframe, command=lambda:(controller.show_frame(StartPage)), bd=0,
                            compound=tk.TOP, image=self.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, bd=0, state=DISABLED, compound=tk.TOP, image=self.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, command=lambda: controller.show_frame(Presense), bd=0,
                            compound=tk.TOP, image=self.add_img3)
        button3.pack(side=tk.LEFT)

        self.img = plt.imread("Perks/e1.png")


        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.verify = False


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

        label = Label(self.leftpanel, text='Type MacAddress or UserName', bd=0, compound=tk.TOP)
        label.pack(side=TOP)

        self.mEntry = Entry(self.leftpanel, textvariable=self.ment)
        self.mEntry.pack(side=TOP, fill=tk.X)
        self.listbox = Listbox(self.leftpanel, width=50, height=20)
        self.scrollbar = tk.Scrollbar(self.listbox, orient="vertical")
        self.scrollbar.pack(side="right", fill="y")


        self.info_label = Label(self)
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.rsum = 0
        self.canvas = FigureCanvasTkAgg(self.f, self)

    def parse(self):
        globals()
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111)
        self.a.imshow(self.img, extent=[0, 1550, 770, 0])


        self.response = self.session.get(hostname + query_active)
        data = self.response.json()

        list = Listbox(self.leftpanel, bd=2, bg='#9DBFC0', width=27, yscrollcommand=self.scrollbar.set,
                       font="Helvetica 16 bold italic", fg = "#3c8081")
        self.scrollbar.config(command=list.yview)
        i = 0
        r = 0

        info_label = Label(self, justify=LEFT, font="Arial 16", fg="#bc5151")

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
                        info_label['text'] = "\n\n\n\nMacAddress:\t\t " + mac['macAddress'] + "\nFloor:\t\t\t "
                        if int(mac['mapInfo']['mapHierarchyString'].find('1st_Floor')) > -1:
                            info_label['text'] += "1st_Floor"
                        else:
                            info_label['text'] += "2nd_Floor"
                        info_label['text'] += "\nRSSI:\t\t\t " + \
                                             str(mac['statistics']['maxDetectedRssi']['rssi']) + "\nSSID:\t\t\t " + \
                                             mac['ssId'] + "\nDevice type:\t\t " + str(mac['manufacturer']) +\
                                             "\nUserName:\t\t " + mac['userName'] + "\nFirst Located Time:\t " +\
                                             mac['statistics']['firstLocatedTime'] + "\nLast Located Time:\t\t " +\
                                             mac['statistics']['lastLocatedTime']
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

            self.info_label.pack_forget()
            self.info_label = info_label
            self.info_label.pack(anchor=NW)
            self.canvas._tkcanvas.pack_forget()
            self.canvas = FigureCanvasTkAgg(self.f, self)
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        if i != self.sum :
            self.sum = i
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
            if not self.listbox.curselection():
                self.info_label.pack_forget()
        self.mEntry.icursor(cur)



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
app.geometry("1600x1200+500+100")
mapi = app.frames[Map]
mapi.parse()
while TRUE:
    mapi.parse()
    app.update()
app.mainloop()
