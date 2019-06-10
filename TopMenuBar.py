
import tkinter as tk
from tkinter import *


def total_visitors_button(top_frame):
    lst_top = Listbox(master=top_frame, width=22, height=4, bg="#99D79C",
                      relief=RAISED, font=("Avenir", 18))
    lst_top.insert(1, "Visitors")
    lst_top.insert(2, "Unique visitors")
    lst_top.insert(3, "Total visitors")
    lst_top.insert(4, "Total Connected")

    def show_listbox(event):
        lst_top.grid(row=1, column=0)

    def hide_listbox(event):
        lst_top.grid_forget()

    lb = Label(top_frame, text='Total Visitors 190', relief=RAISED, bg="#3CC144",
               font=("Avenir", 30), fg='white')
    lb.bind('<Button-1>', show_listbox)
    lb.bind('<Leave>', hide_listbox)
    lb.grid(row=0, column=0, ipadx=50, ipady=10, padx=40, pady=10)


def average_dwell_time_button(top_frame):
    lst_dwell = Listbox(master=top_frame, width=32, height=6, bg='#CA6D6D',
                        font=("Avenir", 18),
                        selectbackground="#A64646", relief=RAISED)
    lst_dwell.insert(1, '5-30 mins')
    lst_dwell.insert(2, '30-60 mins')
    lst_dwell.insert(3, '1-5 hours')
    lst_dwell.insert(4, '5-8 hours')
    lst_dwell.insert(5, '8+ hours')

    # select(lst_box=lst_dwell)

    def show_list(event):
        lst_dwell.grid(row=1, column=1)

    def hide_list(event):
        lst_dwell.grid_forget()

    lb = Label(top_frame, text='Average Dwell Time', relief=RAISED, bg='#B94444',
               font=("Avenir", 30), fg='white')
    lb.bind('<Button-1>', show_list)
    lb.bind('<Leave>', hide_list)
    lb.grid(row=0, column=1, ipadx=50, ipady=10, padx=40, pady=10)


def peak_hour_button(top_frame):
    lst_peak = Listbox(master=top_frame, width=22, height=2, bg='#7ADFE6', font=("Avenir", 18),
                       selectbackground="#3DABB3", relief=RAISED)
    lst_peak.insert(1, "Peak Hour")
    lst_peak.insert(2, 'Visitor count in peak hour')
    lst_peak.select_set(0)
    # select(lst_box=lst_peak)

    def show_peak_list(event):
        lst_peak.grid(row=1, column=2)

    def hide_peak_list(event):
        lst_peak.grid_forget()

    lb = Label(top_frame, text='Peak Hour', relief=RAISED, bg='#22CCD7',
               font=("Avenir", 30), fg='white')
    lb.bind('<Button-1>', show_peak_list)
    lb.bind('<Leave>', hide_peak_list)
    lb.grid(row=0, column=2, ipadx=50, ipady=10, padx=40, pady=10)


def top_device_button(top_frame):
    lst_device = Listbox(master=top_frame, width=32, height=5, bg="#FBD55B", font=("Avenir", 18),
                         selectbackground="#E6BE3E", relief=RAISED)
    lst_device.insert(1, 'Top Device Makers')
    lst_device.insert(2, 'Apple')

    def show_device(event):
        lst_device.grid(row=1, column=3)

    def hide_device(event):
        lst_device.grid_forget()

    lb = Label(master=top_frame, text='Top Device Maker', relief=RAISED, bg='#FFC300',
               font=("Avenir", 30), fg='white')
    lb.bind('<Button-1>', show_device)
    lb.bind('<Leave>', hide_device)
    lb.grid(row=0, column=3, ipadx=50, ipady=10, padx=40, pady=10)
