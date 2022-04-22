# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 16:57:37 2022

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

#%%

class PumpProbe_GUI:
    def __init__(self,Window):
        self.Window = Window
    
        self.Window.title('PumpProbeU21')
        self.Window.minsize(300,200)
        
        filename_var = StringVar()
        filename_var.set('FilePath')
        test_var = StringVar()
        test_var.set('None')
        
        self.f = Frame(self.Window)#,
                       # height = 200,
                       # width = 300)
        self.f.pack(side=BOTTOM)
        
        self.load_button = Button(self.f,text='load Data',command=self.getData)
        self.plot_button = Button(self.f,text='Plot DAS',command=self.plotDAS)
        self.exit_button = Button(self.f,text = 'Exit',command = Window.destroy)
        
        self.filename_label = Label(self.f,text=filename_var)
        
        self.load_button.pack(side=LEFT)
        self.plot_button.pack(side=LEFT)
        self.exit_button.pack(side=LEFT)
    
    
    
    def getData(self):
        self.path = filedialog.askdirectory(initialdir = 'C:/Users/work/Messdaten/U21_TA/20220414_Fe-PDSJS20',
                                                    title = 'Select a file')
        self.data = pp.TreatedData(self.path)
        
        
    def plotDAS(self):
        
        # fig = pp.plotTreatedData(self.data,show=False)
        # fig = Figure(figsize=(5, 4), dpi=100)
        # t = np.arange(0, 3, .01)
        # fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
        
        fig_list=pp.plotTreatedData(self.data,show=False)
        
        fig=Figure()
        for line in fig_list:
            line
        
            
        canvas = FigureCanvasTkAgg(fig, master=self.Window)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        
        

Window=Tk()
PP=PumpProbe_GUI(Window)
Window.mainloop()


