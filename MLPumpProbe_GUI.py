# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 16:57:37 2022

@author: work
"""
import sys
from tkinter import *
# from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from tkintertable import TableCanvas

import numpy as np


# Implement the default Matplotlib key bindings.
# from matplotlib.backend_bases import key_press_handler
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt

import MLPumpProbe as pp
import MLBasic_GUI as GUI

#%%

class PumpProbe_GUI:
    def __init__(self):
        Window=Tk()
        
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
        self.exit_button = Button(self.f,text = 'Exit',command = self.stop)
        
        self.filename_label = Label(self.f,text=filename_var)
        
        self.load_button.pack(side=LEFT)
        self.plot_button.pack(side=LEFT)
        self.exit_button.pack(side=LEFT)
        
        Window.mainloop()
    
    def stop(self):
        self.Window.destroy()
        sys.exit()
    
    def getData(self):
        self.path = GUI.SelectFolder()
        self.data = pp.fitData(self.path)
        
        
    def plotDAS(self):
        
        frame=Frame(self.Window)
        frame.pack()

        fig=self.data.plot(GUI=True)      
            
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        canvas.draw()

        
        

PumpProbe_GUI()



