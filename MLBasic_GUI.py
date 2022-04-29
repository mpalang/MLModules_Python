# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:44:46 2022

@author: work
"""
import tkinter
from tkinter import filedialog
from tkinter import *


def SelectFolder():
    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    path = filedialog.askdirectory()
    
    return path


def SelectFile(multiple=False):
    if multiple:
        files=tkinter.filedialog.askopenfilenames()
    else:
        files=tkinter.filedialog.askopenfilename()
    
    return files

