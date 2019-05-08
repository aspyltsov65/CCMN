import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import messagebox

import Analytics
import calendar_code
import ApiProcess

import calendar
import PIL.ImageTk
import PIL.Image
from datetime import datetime, timedelta, date


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.iconbitmap('@python.xbm')
        tk.Tk.wm_title(self, "CCMN")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.add_img1 = tk.PhotoImage(file='Perks/dashboard_button.gif')
        self.add_img2 = tk.PhotoImage(file='Perks/map_button.gif')
        self.add_img3 = tk.PhotoImage(file='Perks/presense_button.gif')

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
        tk.Frame.__init__(self, parent)
        self["bg"] = "#DCDCDC"
        bottomframe = tk.Frame(self, parent)
        bottomframe["bg"] = '#3c8081'
        bottomframe.pack(side=tk.TOP, fill=tk.X)

        button1 = tk.Button(bottomframe, bd=0, state=DISABLED, compound=tk.TOP, image=controller.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, command=lambda: controller.show_frame(Map),
                            bd=0, compound=tk.TOP, image=controller.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, command=lambda: controller.show_frame(Presense),
                            bd=0, compound=tk.TOP, image=controller.add_img3)
        button3.pack(side=tk.LEFT)


class Map(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["bg"] = "#DCDCDC"
        bottomframe = tk.Frame(self, parent)
        bottomframe["bg"] = '#DCDCDC'
        bottomframe.pack(side=tk.TOP, fill=tk.X)

        button1 = tk.Button(bottomframe, command=lambda: controller.show_frame(StartPage),
                            bd=0, compound=tk.TOP, image=controller.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, bd=0, state=DISABLED, compound=tk.TOP, image=controller.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, command=lambda: controller.show_frame(Presense),
                            bd=0, compound=tk.TOP, image=controller.add_img3)
        button3.pack(side=tk.LEFT)

        self.leftpanel = tk.Frame(self, parent)
        self.leftpanel["bg"] = 'white'
        self.leftpanel.pack(side=LEFT, fill=tk.Y)
        self.ment = StringVar()
        self.leftpanel_switch = tk.Frame(self.leftpanel)
        self.leftpanel_switch.pack(side=TOP)

        self.floor_switch = 1
        self.button_r = tk.Button(self.leftpanel, state=NORMAL,
                                  command=lambda: refresh(self), text='Refresh', bd=0)
        self.button_r.pack(side=TOP, fill=tk.X)

        self.button_s_1 = tk.Button(self.leftpanel_switch, state=NORMAL,
                                    command=lambda: floor_switch(self, 1), text='Floor 1', bd=0, compound=tk.TOP)
        self.button_s_1.pack(side=LEFT)

        self.button_s_3 = tk.Button(self.leftpanel_switch, state=NORMAL,
                                    command=lambda: floor_switch(self, 3), text='Floor 3', bd=0, compound=tk.TOP)
        self.button_s_3.pack(side=RIGHT)

        self.button_s_2 = tk.Button(self.leftpanel_switch, state=NORMAL,
                                    command=lambda: floor_switch(self, 2), text='Floor 2', bd=0, compound=tk.TOP)
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
        self.onfloor_total = Label(self, justify=LEFT, font="Arial 16", fg="#bc5151",anchor=S)

    def parse(self):
        globals()
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.a = self.f.add_subplot(111, title="")
        self.img = plt.imread("Perks/e1.png")

        self.f.gca().axes.get_yaxis().set_visible(False)
        self.f.gca().axes.get_xaxis().set_visible(False)
        self.a.imshow(self.img, extent=[0, 1550, 770, 0])

        list = Listbox(self.leftpanel, bd=2, bg='#9DBFC0', width=27,
                       font="Helvetica 16 bold italic", fg="#3c8081")
        info_label = Label(self, justify=LEFT, font="Arial 16", fg="#bc5151", anchor=SW)
        typed_text = self.ment.get()
        onfloor_total = Label(self.leftpanel, justify=LEFT, font="Arial 16", fg="#3c8081", anchor=S)
        onfloor = 0
        total = 0

        data = ApiProcess.get_active()

        for mac in data:
            if self.listbox.curselection() and (
                    mac['macAddress'] in str(self.listbox.get((self.listbox.curselection())))
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
                onfloor += 1
            if mac['ipAddress']:
                total += 1
            if not mac['macAddress'] in self.connected and mac['ipAddress']:
                self.connected += mac['macAddress']

                if " " in self.connected and '1' in mac['mapInfo']['mapHierarchyString']:
                    messagebox.showinfo("Notification",
                                        mac['macAddress'] + " " + mac['userName'] + " now is on the first floor")
                elif " " in self.connected and '2' in mac['mapInfo']['mapHierarchyString']:
                    messagebox.showinfo("Notification",
                                        mac['macAddress'] + " " + mac['userName'] + " now is on the second floor")
                elif " " in self.connected and '3' in mac['mapInfo']['mapHierarchyString']:
                    messagebox.showinfo("Notification",
                                        mac['macAddress'] + " " + mac['userName'] + " now is on the third floor")
        self.connected += " "
        onfloor_total['text'] = "On floor: " + str(onfloor) + "/ total: " + str(total)
        self.onfloor_total.pack_forget()
        self.onfloor_total = onfloor_total
        self.onfloor_total.pack(side=tk.TOP)
        if self.listbox.curselection():
            if str(self.listbox.get(self.listbox.curselection())) in str(list.get(self.listbox.curselection())):
                list.selection_set(self.listbox.curselection())
        if list:
            self.listbox.pack_forget()
            self.listbox = list
            if list.curselection():
                self.listbox.selection_set(list.curselection())
            self.listbox.pack(side=LEFT, fill=Y)
        if self.cur_selection != self.listbox.curselection():
            self.cur_selection = self.listbox.curselection()
            self.canvas._tkcanvas.pack_forget()
            self.canvas = FigureCanvasTkAgg(self.f, self)
            self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        if not self.listbox.curselection():
            self.info_label.pack_forget()
        else:
            self.info_label.pack_forget()
            self.info_label = info_label
            self.info_label.pack(anchor=SW)


class Presense(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self["bg"] = "#DCDCDC"
        bottomframe = tk.Frame(self, parent)
        bottomframe["bg"] = 'white'
        bottomframe.pack(side=tk.TOP, fill=tk.X)
        button1 = tk.Button(bottomframe, command=lambda: controller.show_frame(StartPage),
                            bd=0, compound=tk.TOP, image=controller.add_img1)
        button1.pack(side=tk.LEFT)

        button2 = tk.Button(bottomframe, command=lambda: controller.show_frame(Map),
                            bd=0, compound=tk.TOP, image=controller.add_img2)
        button2.pack(side=tk.LEFT)

        button3 = tk.Button(bottomframe, bd=0, state=DISABLED, compound=tk.TOP, image=controller.add_img3)
        button3.pack(side=tk.LEFT)

        self.datato = {'date': "2019-5-4"}
        self.datafrom = {'date': "2019-5-2"}
        self.parent = parent
        self.to_btn = tk.Button(bottomframe, text='ᐁ', command=lambda: self.popup(1), bg='white')
        self.to_btn.pack(side=tk.RIGHT, fill=tk.Y)

        self.to_date = Label(bottomframe, text=self.datato['date'], bd=2, bg='white')
        self.to_date.pack(side=tk.RIGHT, fill=tk.Y)

        self.from_btn = tk.Button(bottomframe, text='ᐁ', command=lambda: self.popup(2), bg='white')
        self.from_btn.pack(side=tk.RIGHT, fill=tk.Y)

        self.from_date = Label(bottomframe, text=self.datafrom['date'], bd=2, bg='white')
        self.from_date.pack(side=tk.RIGHT, fill=tk.Y)
        self.top = tk.Frame(self, parent, bg='#76C019')
        self.middle = tk.Frame(self, parent)
        self.bot = tk.Frame(self, parent)
        self.top.pack(side=TOP, fill=tk.X)
        self.middle.pack()
        self.bot.pack(side=BOTTOM)

        # self.peak_hour1 = Label(self.top, text='Peak hour today:', font=("Bookman", 20),
        #                         bg='#3c8081')
        # self.peak_hour2 = Label(self.top, text=str(ApiProcess.get_peak()) + ':00', font=("Bookman", 25),
        #                         fg='#FFA505', bg='#3c8081')
        # self.peak_hour1.pack(side=LEFT, fill=tk.Y)
        # self.peak_hour2.pack(side=LEFT)
        #
        # self.count_visitors1 = Label(self.top, text='   Count of visitors today:', font=("Bookman", 20),
        #                              bg='#3c8081')
        # self.count_visitors2 = Label(self.top, text=str(ApiProcess.get_today_visitors()), font=("Bookman", 25),
        #                              fg='#FFA505', bg='#3c8081')
        # self.count_visitors1.pack(side=LEFT, fill=tk.Y)
        # self.count_visitors2.pack(side=LEFT)
        #
        # self.count_yes_visitors1 = Label(self.top, text='   Count of visitors yesterday:', font=("Bookman", 20),
        #                                  bg='#3c8081')
        # self.count__yes_visitors2 = Label(self.top, text=str(ApiProcess.get_today_visitors()), font=("Bookman", 25),
        #                                   fg='#FFA505', bg='#3c8081')
        # self.count_yes_visitors1.pack(side=LEFT, fill=tk.Y)
        # self.count__yes_visitors2.pack(side=LEFT)

        # fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
        # self.canvas_dwell = FigureCanvasTkAgg(fig, self.middle)
        # self.canvas_repeat = FigureCanvasTkAgg(fig, self.middle)
        # self.make_peak_hour()
        Analytics.connected_visitors(self.from_date, self.to_date, self.middle)
        Analytics.repeat_visitors(self.from_date, self.to_date, self.middle)
        # Analytics.correlation_day_students()


    def popup(self, sw):
        child = tk.Toplevel()
        child.geometry("255x310+1845+170")
        if sw == 1:
            cal = calendar_code.calen(child, self.datato, self, sw)
        else:
            cal = calendar_code.calen(child, self.datafrom, self, sw)



def close_window():
    global running
    running = False
    app.destroy()


def label_paste(info_label, mac):
    info_label['text'] = "\tMacAddress:\t\t " + mac['macAddress'] + "\n\tFloor:\t\t\t "
    if '1st_Floor' in mac['mapInfo']['mapHierarchyString']:
        info_label['text'] += "First floor"
    elif '2nd_Floor' in mac['mapInfo']['mapHierarchyString']:
        info_label['text'] += "Second floor"
    else:
        info_label['text'] += "Third floor"
    info_label['text'] += "\n\tRSSI:\t\t\t " + \
        str(mac['statistics']['maxDetectedRssi']['rssi']) + "\n\tSSID:\t\t\t " + \
        mac['ssId'] + "\n\tDevice type:\t\t " + str(mac['manufacturer']) + \
        "\n\tUserName:\t\t " + mac['userName'] + "\n\tFirst Located Time:\t " + \
        mac['statistics']['firstLocatedTime'] + "\n\tLast Located Time:\t\t " + \
        mac['statistics']['lastLocatedTime'] + "\n\n\n"


def floor_switch(self, cont):
    if cont == 1:
        self.img = plt.imread("Perks/e1.png")
    elif cont == 2:
        self.img = plt.imread("Perks/e2.png")
    else:
        self.img = plt.imread("Perks/e3.png")
    self.floor_switch = cont
    if self.listbox.curselection():
        self.listbox.selection_clear(self.listbox.curselection())
    self.sum = 0
    refresh(self)


def refresh(self):
    self.cur_selection = None


if __name__ == "__main__":

    running = True

    app = SeaofBTCapp()
    app.geometry("1600x1200+500+100")
    app.protocol("WM_DELETE_WINDOW", close_window)
    app.bind('<Escape>', lambda e: close_window())

    # print(type(date.today()))
    # print(calendar.day_name[date.today().weekday()])
    # print(datetime.now() - timedelta(days=7))
    mapi = app.frames[Map]
    mapi.parse()

    while running:
        mapi.parse()
        app.update()
