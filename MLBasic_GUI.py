# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 10:44:46 2022

@author: work
"""
from tkinter import *
from tkinter import filedialog as fd
from tkinter import simpledialog as sd


#%%

def MsgBox(text,title=None):
    root=Tk()
    root.minsize(50,50)
    
    tk.Label(root,text=text,title=title).pack(padx=20, pady=20, anchor=CENTER)
    
    root.mainloop()


def SelectFolder():
    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    path = fd.askdirectory()
    
    return path


def SelectFile(multiple=False,title=None,path=None):
    root = Tk()
    root.wm_attributes('-topmost', 1)
    root.withdraw()
    if multiple:
        files=fd.askopenfilenames(title=title,initialdir=path)
    else:
        files=fd.askopenfilename(title=title,initialdir=path)
    
    return files


#%%

class IntInput:
    def __init__(self,Number=1,Label=[]):
        self.root=Tk()
        
        self.Label=Label
        self.intVars=[]
        
        EntryFrame=Frame(self.root)
        for n in range(Number):
            self.addEntry(EntryFrame,n)
        
        ButtonFrame=Frame(self.root)
        Button(ButtonFrame,text='ok',command=self.ok).pack(side=LEFT,expand=YES,padx=5,pady=5)
        Button(ButtonFrame,text='Exit',command=self.root.destroy).pack(side=LEFT,expand=YES,padx=5,pady=5)
        
        EntryFrame.pack(side=TOP)
        ButtonFrame.pack(side=TOP)
        
        self.root.mainloop()
        
    def ok(self):
        self.Vars=[]
        for i in self.intVars:
            self.Vars.append(i.get())
        self.root.destroy()

    
    def addEntry(self,frame,n):
        ElementFrame=Frame(frame)
        ElementFrame.pack(side=TOP)
        
        self.intVars.append(IntVar())
        if len(self.Label)>0:
            Label(ElementFrame,text=self.Label[n]).pack(side=LEFT,padx=5,pady=5)
        Entry(ElementFrame,textvariable=self.intVars[n]).pack(side=LEFT,padx=5,pady=5)
        
        


#%%

class StrInput:
    def __init__(self,Number=1,Label=[]):
        self.root=Tk()
        self.root.title('Input Strings')
        
        self.Label=Label
        self.intVars=[]
        
        EntryFrame=Frame(self.root)
        for n in range(Number):
            self.addEntry(EntryFrame,n)
        
        ButtonFrame=Frame(self.root)
        Button(ButtonFrame,text='ok',command=self.ok).pack(side=LEFT,expand=YES,padx=5,pady=5)
        Button(ButtonFrame,text='Exit',command=self.root.destroy).pack(side=LEFT,expand=YES,padx=5,pady=5)
        
        EntryFrame.pack(side=TOP)
        ButtonFrame.pack(side=TOP)
        
        self.root.mainloop()
        
    def ok(self):
        self.Vars=[]
        for i in self.intVars:
            self.Vars.append(i.get())
        self.root.destroy()
        

    
    def addEntry(self,frame,n):
        ElementFrame=Frame(frame)
        ElementFrame.pack(side=TOP)
        
        self.intVars.append(StringVar())
        if len(self.Label)>0:
            Label(ElementFrame,text=self.Label[n]).pack(side=LEFT,padx=5,pady=5)
        Entry(ElementFrame,textvariable=self.intVars[n]).pack(side=LEFT,padx=5,pady=5)
        

        
    
    
    
