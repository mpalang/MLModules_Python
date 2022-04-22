# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 18:32:25 2022

@author: work
"""

from tkinter import *
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkintertable import TableCanvas

import pandas as pd
from pandastable import Table
import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import MLPumpProbe as pp


def plot():
    
    x=np.arange(0,100,1)
    y=np.sin(x)
    
    fig=Figure()
    plt.plot(x,y)
    plt.plot(x,-y)
    

    
    return fig


Window=Tk()

plots=plot()
fig=Figure()
fig.add_subplot(111).plots
# fig.show()
canvas = FigureCanvasTkAgg(fig, master=Window)  # A tk.DrawingArea.
canvas.draw()
canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

Window.mainloop()



