
import tkinter as tk
from tkinter import *
import ApiProcess


def total_visitors_button(top_frame):
    lst_top = Listbox(master=top_frame,
                      width=22,
                      height=4,
                      bg="#99D79C",
                      selectbackground="#5EAA5A",
                      relief=RAISED,
                      font=("Avenir", 18))

    items_for_listbox = ["Visitors",
                         "Unique visitors   " + str(ApiProcess.get_today_visitors()),
                         "Total visitors    " + str(ApiProcess.get_today_visitors()),
                         "Total Connected   " + str(ApiProcess.get_total_connected())]

    for items in items_for_listbox:
        lst_top.insert(END, items)

    # lst_top.select_set(0)

    def show_listbox(event):
        lst_top.grid(row=1, column=0)

    def hide_listbox(event):
        lst_top.grid_forget()

    lb = Label(top_frame, text='Total Visitors ' + str(ApiProcess.get_today_visitors()),
               relief=RAISED,
               bg="#3CC144",
               font=("Avenir", 30),
               fg='white')

    lb.bind('<Button-1>', show_listbox)
    lb.bind('<Leave>', hide_listbox)
    lb.grid(row=0, column=0, ipadx=20, ipady=10, padx=20, pady=10)


def average_dwell_time_button(top_frame):
    lst_dwell = Listbox(master=top_frame,
                        width=32,
                        height=6,
                        bg='#CA6D6D',
                        font=("Avenir", 18),
                        selectbackground="#A64646",
                        relief=RAISED)

    items_for_listbox = ['5-30 mins ' + str(ApiProcess.get_count_of_visitors_by_dwell_level_for_today()["FIVE_TO_THIRTY_MINUTES"]),
                         '30-60 mins ' + str(ApiProcess.get_count_of_visitors_by_dwell_level_for_today()["THIRTY_TO_SIXTY_MINUTES"]),
                         '1-5 hours ' + str(ApiProcess.get_count_of_visitors_by_dwell_level_for_today()["ONE_TO_FIVE_HOURS"]),
                         '5-8 hours ' + str(ApiProcess.get_count_of_visitors_by_dwell_level_for_today()["FIVE_TO_EIGHT_HOURS"]),
                         '8+ hours ' + str(ApiProcess.get_count_of_visitors_by_dwell_level_for_today()["EIGHT_PLUS_HOURS"])]

    for items in items_for_listbox:
        lst_dwell.insert(END, items)

    # lst_dwell.select_set(0)

    def show_list(event):
        lst_dwell.grid(row=1, column=1)

    def hide_list(event):
        lst_dwell.grid_forget()

    lb = Label(master=top_frame,
               text='Average Dwell Time ' + str(round(ApiProcess.get_average_visitor_dwell_time_for_today())) + " mins",
               relief=RAISED,
               bg='#B94444',
               font=("Avenir", 30),
               fg='white')

    lb.bind('<Button-1>', show_list)
    lb.bind('<Leave>', hide_list)
    lb.grid(row=0, column=1, ipadx=20, ipady=10, padx=20, pady=10)


def peak_hour_button(top_frame):
    lst_peak = Listbox(master=top_frame,
                       width=30,
                       height=2,
                       bg='#7ADFE6',
                       font=("Avenir", 18),
                       selectbackground="#3DABB3",
                       relief=RAISED)

    lst_peak.insert(1, "Peak Hour" )
    lst_peak.insert(2, 'Visitor count in peak hour 162')

    # lst_peak.select_set(0)

    def show_peak_list(event):
        lst_peak.grid(row=1, column=2)

    def hide_peak_list(event):
        lst_peak.grid_forget()

    lb = Label(master=top_frame,
               text='Peak Hour 4pm-5pm',                                           # create get request and parse data
               relief=RAISED,
               bg='#22CCD7',
               font=("Avenir", 30),
               fg='white')

    lb.bind('<Button-1>', show_peak_list)
    lb.bind('<Leave>', hide_peak_list)
    lb.grid(row=0, column=2, ipadx=20, ipady=10, padx=20, pady=10)


def top_device_button(top_frame):
    lst_device = Listbox(master=top_frame,
                         width=32,
                         height=6,
                         bg="#FBD55B",
                         font=("Avenir", 18),
                         selectbackground="#E6BE3E",
                         relief=RAISED)

    lst_device.insert(1, 'Top Device Makers')
    lst_device.insert(2, 'Apple 47 visitors')
    lst_device.insert(3, 'Samsung 7 visitors')
    lst_device.insert(4, 'Shanghai Wind Technologies 6 visitors')
    lst_device.insert(5, 'Intel 5 visitors')
    lst_device.insert(6, 'Shanghai Huaqin 4 visitors')

    lst_device.select_set(0)

    def show_device(event):
        lst_device.grid(row=1, column=3)

    def hide_device(event):
        lst_device.grid_forget()

    lb = Label(master=top_frame,
               text='Top Device Maker Apple',
               relief=RAISED,
               bg='#FFC300',
               font=("Avenir", 30),
               fg='white')

    lb.bind('<Button-1>', show_device)
    lb.bind('<Leave>', hide_device)
    lb.grid(row=0, column=3, ipadx=20, ipady=10, padx=20, pady=10)
