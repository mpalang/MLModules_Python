# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 17:28:36 2022

@author: work
"""

import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox as msg
from pandastable import Table
from tkintertable import TableCanvas
import numpy as np
   
  
class csv_to_excel:
   
    def __init__(self, root):
   
        self.root = root
        # self.file_name = ''
        self.f = Frame(self.root,
                       height = 200,
                       width = 300)
          
        # Place the frame on root window
        self.f.pack()
           
        # Creating label widgets
        # self.message_label = Label(self.f,
        #                            text = 'GeeksForGeeks',
        #                            font = ('Arial', 19,'underline'),
        #                            fg = 'Green')
        
        # self.message_label2 = Label(self.f,
        #                             text = 'Converter of CSV to Excel file',
        #                             font = ('Arial', 14,'underline'),
        #                             fg = 'Red')
   
        # Buttons
        self.load_button = Button(self.f,
                                     text = 'Load Data',
                                     font = ('Arial', 14),
                                     bg = 'Orange',
                                     fg = 'Black',
                                     command = self.load_Data)
        self.display_button = Button(self.f,
                                     text = 'Display',
                                     font = ('Arial', 14), 
                                     bg = 'Green',
                                     fg = 'Black',
                                     command = self.display_xls_file)
        self.exit_button = Button(self.f,
                                  text = 'Exit',
                                  font = ('Arial', 14),
                                  bg = 'Red',
                                  fg = 'Black', 
                                  command = root.destroy)
   
        # Placing the widgets using grid manager
        # self.message_label.grid(row = 1, column = 1)
        # self.message_label2.grid(row = 2, column = 1)
        self.load_button.grid(row = 3, column = 0,
                                 padx = 0, pady = 15)
        self.display_button.grid(row = 3, column = 1, 
                                 padx = 10, pady = 15)
        self.exit_button.grid(row = 3, column = 2,
                              padx = 10, pady = 15)
   
    def load_Data(self):
        try:
            self.file_name = filedialog.askopenfilename(initialdir = 'C:/Users/work/Messdaten/U21_TA/20220414_Fe-PDSJS20',
                                                        title = 'Select a CSV file')#filetypes = (('csv file','*.csv'),('csv file','*.csv')))
               
            self.data = np.loadtxt(self.file_name)
                  
               
        except FileNotFoundError as e:
                msg.showerror('Error in opening file', e)
   
    def display_xls_file(self):
        
        try:      
            # Now display the DF in 'Table' object
            # under'pandastable' module
            df = pd.DataFrame(self.data)
            self.f2 = Frame(self.root, height=200, width=300) 
            self.f2.pack(fill=BOTH,expand=1)
            self.table = Table(self.f2, dataframe=df,read_only=True)
            self.table.show()
          
        except FileNotFoundError as e:
            print(e)
            msg.showerror('Error in opening file',e)
  
# Driver Code 
root = Tk()
root.title('GFG---Convert CSV to Excel File')
   
obj = csv_to_excel(root)
root.geometry('800x600')
root.mainloop()