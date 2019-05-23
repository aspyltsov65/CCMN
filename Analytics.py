import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import ApiProcess

import start


# def make_peak_hour(self):
#     self.peak = tk.Frame(self, self.top, bg='#76C019')
#     self.peak.pack(side='left')
#
#     self.fig = Figure(figsize=(2, 2), dpi=100)
#     self.sub = self.fig.add_subplot(111, title="")
#     self.img = plt.imread("Perks/clock.png")
# #
# #     self.canv = FigureCanvasTkAgg(self.fig, self)
# #     self.canv._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
#
# # im = PIL.Image.open("Perks/e1.png")
# # logo = PIL.ImageTk.PhotoImage(im)
# # add_peak_logo = Label(self.top, image=logo)
# # add_peak_logo.image = logo
# # add_peak_logo.pack(side='left')
# #
# # self.human_logo = plt.imread("Perks/e1.png")
# # add_title = Label(self.top, text='Peak hour: ', font=("Bookman", 20), bg='#76C019')
# # value = Label(self.top, text=str(ApiProcess.get_peak()) + ':00', font=("Bookman", 25),
# #               fg='#FFFFFF', bg='#76C019')
# # # add_peak_logo.pack(side='left')
# # add_title.pack(side='left')
# # value.pack(side='left')
#
# # self.peak.pack(side=TOP)
#
def put_dwell(middle_frame, figure, direction):
    canvas_repeat = FigureCanvasTkAgg(figure, middle_frame)
    canvas_repeat._tkcanvas.pack(side=direction)


def func(pct, allvals):
    absolute = int(pct / 100. * np.sum(allvals))
    return "{:d}".format(absolute)


def connected_visitors(from_date, to_date, middle_frame):
    data = ApiProcess.get_presence(from_date['text'], to_date['text'])

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(aspect="equal"), dpi=100)

    recipe = [str(data['FIVE_TO_THIRTY_MINUTES']) + " 5-30minutes",
              str(data['THIRTY_TO_SIXTY_MINUTES']) + " 30-60minutes",
              str(data['ONE_TO_FIVE_HOURS']) + " 1-5hours",
              str(data['FIVE_TO_EIGHT_HOURS']) + " 5-8hours",
              str(data['EIGHT_PLUS_HOURS']) + " 8+hours"]

    dat = [float(x.split()[0]) for x in recipe]
    ingredients = [x.split()[-1] for x in recipe]

    wedges, texts, autotexts = ax.pie(dat, autopct=lambda pct: func(pct, dat),
                                      textprops=dict(color="w"))
    ax.legend(wedges, ingredients,
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=9, weight="bold")

    ax.set_title("Connected Visitors Dwell Time:")
    fig.set_facecolor('#FFFFFF')
    put_dwell(middle_frame, fig, 'right')


def repeat_visitors(from_date, to_date, middle_frame):
    data = ApiProcess.get_repeat_visitors(from_date['text'], to_date['text'])

    fig, ax = plt.subplots(figsize=(8, 6), subplot_kw=dict(aspect="equal"), dpi=100)

    recipe = [str(data['DAILY']) + " DAILY",
              str(data['WEEKLY']) + " WEEKLY",
              str(data['OCCASIONAL']) + " OCCASIONAL",
              str(data['FIRST_TIME']) + " FIRST_TIME",
              str(data['YESTERDAY']) + " YESTERDAY"]

    dat = [float(x.split()[0]) for x in recipe]
    ingredients = [x.split()[-1] for x in recipe]

    wedges, texts, autotexts = ax.pie(dat, autopct=lambda pct: func(pct, dat),
                                      textprops=dict(color="w"))

    ax.legend(wedges, ingredients,
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=9, weight="bold")

    ax.set_title("Repeat visitors:")
    fig.set_facecolor('#FFFFFF')
    put_dwell(middle_frame, fig, 'left')


def correlation_day_students():
    data = ApiProcess.get_day_count_students()

    fig, axs = plt.s()
    print(data.keys())
