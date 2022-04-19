# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 10:50:26 2022

@author: work
"""

from pathlib import Path
import csv
import copy
from glob import glob
from re import search

import numpy as np

from MLModules.MLPlot import MLplot as plot
from MLModules.MLPlot import MLcontour as contour


#%%

folderpath = r"C:\Users\work\Messdaten\U21_TA\20220414"
filepath = r"C:\Users\work\Messdaten\U21_TA\20220414\05_transient_ma.dat"
folderpath = Path(folderpath.replace("\\","/"))
filepath = Path(filepath.replace("\\","/"))

#%% Raw Data:


def getRawData(filepath,folderpath):

    transient = np.loadtxt(Path(filepath), delimiter='\t')
    dt = transient[0,:]
    transient = transient[1:,:]
    
    WL = np.loadtxt(Path(folderpath,'Calibration', 'WavelengthTable.dat'), delimiter='\t')[:,1]
    
    return dt,WL,transient


def correctFlip(dt,WL,transient,position):
    
    transient_c=transient
    transient_c[:,:position]=1/transient[:,:position]
    
    data=np.column_stack(WL,transient_c)
    
    np.savetxt(Path(filepath,'transient_corrected.dat'), data, delimiter='\t', fmt='%1.8f')
    
    return transient_c
    
    

#%% Visualization:

# contour(static,zmin=0,zmax=2)

def plotPP(dt,WL,transient,static):
    contour(None,None,transient,zmin=-0.3,zmax=0.2)
    
    #dt in ps:
    dtmin=0
    dtmax=10
    step=30
    
    dtmin_index=np.where(dt>dtmin)[0][0]
    dtmax_index=np.where(dt>dtmax)[0][0]
    
    # plot(WL[0:420],ta[0:420,dtmin_index:dtmax_index:step],ymin=-0.5,ymax=0.5, label=dt[dtmin_index:dtmax_index:step])
    # 

#%% Save Data:
  
def SaveData(dt,WL,transient):
    data = np.vstack((dt,transient))
    
    np.savetxt(Path(filepath,'transient_corrected.dat'), data, delimiter='\t', fmt='%1.8f')
    np.savetxt(Path(filepath,'transient_corrected_T.dat'), data.T, delimiter='\t', fmt='%1.8f')
    
#%% Remove Spikes:

#%%

def FitPlot(filepath):
    
    filename='transient_cc_WL_clip_OD'
    
    # with open('eggs.csv', newline='') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    #     for row in spamreader:
    #         spam.append(row)
    
    fit_cont = np.genfromtxt(Path(filepath,filename+'.fit'), delimiter='\t')
    
    fit=copy.copy(fit_cont[1:,1:])
    dt=fit_cont[0,1:]
    WL=fit_cont[1:,0]
    
    amp = np.genfromtxt(Path(filepath,filename+'.amplitudes'), delimiter='\t', skip_header=4)
    
    contour(WL,dt,fit)
    
    return dt,WL,fit,amp

    
class CalcPump():
    def __init__(self, meanPower: 'Power measured before chopper in uW', pulse_diameter: 'in um (gaussian)'= 10, wavelength: 'in nm' = 400,repetition_rate:'in Hz' = 1000, fraction_of_blocked_pulses = 0.5):
    
        self.Pulse_Energy = (meanPower/(repetition_rate*fraction_of_blocked_pulses), 'uJ')
        
        planck = (6.62607015E-34, 'm^2*kg/s')
        self.Pulse_Diameter = (pulse_diameter, 'um')
        self.Pump_Area = (np.pi*(pulse_diameter/2)**2, 'um^2')
        self.Fluency = (self.Pulse_Energy[0]/(self.Pump_Area[0]), 'Photons/cm^2')
    
    
    # for var in vars():
    #     print(var)

    
#%% Fitted Data:
    
class getTreatedData :
    def __init__(self,folderpath):
        
    
        files = glob(str(Path(folderpath,'*')))
        self.No_Comp=0
        self.tau=[]
        self.DAS = []
        
        
        
        for f in files:
            
            if 'parameter' in f:
                with open(f,'r') as readfile:
                    self.text = readfile.readlines()
                
                
                for line in self.text:
                    if 'A_' in line and '1.0' in line:
                        self.No_Comp+=1
                    
                for n in range(self.No_Comp):
                    for line in self.text:
                        if 'tau_'+str(n+1) in line:
                            self.tau.append(float(search('([0-9]+[.])[0-9]+',line).group()))
                            
                        
        for f in files:
           
            if 'amplitudes' in f:
                data = np.genfromtxt(Path(f), delimiter='\t',skip_header=4)
                self.DAS_WL = data[:,0]
                
                
                for n in range(self.No_Comp):
                    self.DAS.append(data[:,n+1])

                
            elif '.dat' in f and 'cc' in f:
                data = np.genfromtxt(f)
                self.WL = data[0,1:]
                self.dt = data[:,1:]
                self.TA = data[1:,1:]

def plotTreatedData(data):
    
    plot(data.DAS_WL,data.DAS, label=[str(i)+' ps' for i in data.tau], separate=False)
    
    
