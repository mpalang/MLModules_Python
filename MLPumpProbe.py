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

folderpath = [r"C:\Users\work\Messdaten\U21_TA\20220422_Berkefeld\12_short",
              r"C:\Users\work\Messdaten\U21_TA\20220422_Berkefeld\13_long"]
              
              


# filepath = r"C:\Users\work\Messdaten\U21_TA\20220414_Fe-PDSJS20\05_transient_ma.dat"
# folderpath = Path(folderpath.replace("\\","/"))
# filepath = Path(filepath.replace("\\","/"))

#%% Raw Data:
def plotRawData(dt,WL,transient,static,title=None):
    
    contour(None,WL,transient,zmin=0.95,zmax=1.05,title=title)
    contour(None,None,static,zmin=0,zmax=1,title=title)

class RawData:
    def __init__(self,folderpath,plot=True,signal_strength='weak'):
        
        if signal_strength=='weak':
    
        folderpath = folderpath.replace('\\','/')
        title = Path(folderpath).name
        
        self.path = folderpath
        t_path = glob(str(Path(folderpath,'raw','*transient*')))[0]
        s_path = glob(str(Path(folderpath,'raw','*static*')))[0]
        
        transient = np.loadtxt(Path(t_path), delimiter='\t')
        self.dt = transient[0,:]
        self.transient = transient[1:,:]
        
        static = np.loadtxt(Path(s_path), delimiter='\t')
        
        self.t = static[0,:]
        self.static = static[1:,:]
        
        self.WL = np.loadtxt(Path(folderpath,'..','Calibration','WavelengthTable.dat'), delimiter='\t')[:,1]

        if plot:
            contour(None,None,self.transient,zmin=0.995,zmax=1.005,title=Path(self.path).name)


def correctFlip(data,position,direction, path):
    
    transient_c=data.transient
    
    if direction=='before':
        transient_c[:,:position]=1/data.transient[:,:position]
    if direction=='after':
        transient_c[:,position:]=1/data.transient[:,position:]
    
    data=np.column_stack((data.WL,transient_c))
    data=np.vstack((np.insert(dt,0,0),data))
    
    np.savetxt(Path(path), data, delimiter='\t', fmt='%1.8f')
    
    return transient_c



def plotFlip(transient,xmin,xmax):
    
    for n in range(xmin,xmax,1):
        plot(None,transient[:,n],ymin=0.95, ymax=1.05, title=str(n))
        
    position = input('position= ')
    direction = input('direction= ')
    

def SaveData(dt,WL,transient,folderpath):
    data = np.vstack((dt,transient))
    
    np.savetxt(Path(folderpath,'transient_fc.dat'), data, delimiter='\t', fmt='%1.8f')
    np.savetxt(Path(folderpath,'transient_fc_T.dat'), data.T, delimiter='\t', fmt='%1.8f')
    
#%% Execute RawData Functions here:
    
# dt_ma, WL, transient_ma,t_ma, static_ma, t_path = getRawData(Path(folderpath,'05_ma'))   
# transient_c = correctFlip(dt_ma,WL,transient_ma,1144,'before',Path(str(t_path).replace('.dat','')+'_fc.dat')) 

data={}
for path in folderpath:
    data[Path(path).name]=RawData(path)
    
#%% Remove Spikes:

#%% Calculate


    
#%% Fitted Data:
    
class TreatedData :
    def __init__(self,folderpath):
        
        folderpath = folderpath.replace("\\","/")
    
        files = glob(str(folderpath)+'/**/*', recursive=True)
        self.No_Comp=0
        self.tau=[]
        self.DAS = []
        self.path = folderpath
        
        WLTablepath = glob(str(Path(Path(folderpath).parent,'Calibration/*WaveLengthTable*')),recursive=True)[0]
        self.WavelengthTable = np.loadtxt(WLTablepath,delimiter='\t')
        
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

            if '.fit' in f:
                data = np.genfromtxt(Path(f), delimiter='\t',)
                self.fit = data
    
            elif '.dat' in f and 'cc' in f:
                data = np.genfromtxt(f)
                self.WL = data[0,1:]
                self.dt = data[1:,0]
                self.TA = data[1:,1:]
            
            elif 'static' in f:
                data = np.genfromtxt(f)
                self.static = data[1:,:]
                self.static_t = data[0,:]
                
        # Abspath = glob(str(Path(Path(folderpath).parent,'*Abs*.dat')))[0]
        
        # if len(Abspath)>0:
        #         data = np.genfromtxt(Abspath, delimiter=';')
        #         self.Abs_WL = data[:,0]
        #         self.Abs = data[:,1]
                
        

def plotTreatedData(data,inverse=False,show=True):
    
    if inverse:
        for n,i in enumerate(data.DAS):
            data.DAS[n]=(-1)*data.DAS[n]
            
    fig=plot(data.DAS_WL,data.DAS, 
         label=[str(i)+' ps' for i in data.tau], 
         separate=False, title=str(Path(data.path).name), 
         xlabel='WL/nm', ylabel=r'$\Delta$OD', 
          # Abs=(data.Abs_WL,data.Abs),
         # static=(data.WavelengthTable[:,1],np.mean(data.static,axis=1)),
         show=show
         )
    
    return fig
    
#%% Execute Treated Data Functions:
    
# ma = TreatedData(r'C:\Users\work\Messdaten\U21_TA\20220421_Berkefeld\02_ma')
# plotTreatedData(ma,inverse=False)

# perp = TreatedData(r'C:\Users\work\Messdaten\U21_TA\20220414_Fe-PDSJS20\03_perp')
# plotTreatedData(perp)

# para = TreatedData(r'C:\Users\work\Messdaten\U21_TA\20220414_Fe-PDSJS20\06_parallel')
# plotTreatedData(para)