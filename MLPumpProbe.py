# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 10:50:26 2022

@author: Moritz Lang

In this Module I created some helpful functions and classes to deal with Data from 
pump-probe experiments as obtained in U21- AG Lochbrunner.
"""

from pathlib import Path
import csv
import copy
from glob import glob
from re import search
import sys

import numpy as np

from MLModules.MLPlot import MLplot as plot
from MLModules.MLPlot import MLcontour as contour
import MLModules.MLBasic_GUI as GUI

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("Logging.log"),
        logging.StreamHandler(sys.stdout)
    ])



#%% Here you can specify some file or folderpaths if needed.

# folderpath = [r"C:\Users\work\Messdaten\U21_TA\20220422_Berkefeld\12_short",
#               r"C:\Users\work\Messdaten\U21_TA\20220422_Berkefeld\13_long"]
# filepath = r"C:\Users\work\Messdaten\U21_TA\20220414_Fe-PDSJS20\05_transient_ma.dat"
# folderpath = Path(folderpath.replace("\\","/"))
# filepath = Path(filepath.replace("\\","/"))

#%% Raw Data:




def SubtractSolvent(filepath=None):
    """
    Thsi function subtracts absorption spectra of solvents.

    """
     
    path = GUI.SelectFolder() 
    files = glob.glob(str(Path(path,'*.csv')))
    return files
    
   

class RawData:
    """ 
    This class fetches all the needed Raw Data.
    """
    
    def __init__(self,folderpath=None,signal_strength='weak'):
        

        if folderpath==None:
            folderpath = GUI.SelectFolder() 
            
        folderpath = folderpath.replace('\\','/')
        title = Path(folderpath).name
        filelist=glob(str(folderpath)+'/**/*', recursive=True)
        
        self.path = folderpath
        self.t_path = glob(str(Path(folderpath,'raw','*transient*')))[0]
        self.s_path = glob(str(Path(folderpath,'raw','*static*')))[0]
        
        transient = np.loadtxt(Path(self.t_path), delimiter='\t')
        self.dt = transient[0,:]
        self.transient = transient[1:,:]
        
        static = np.loadtxt(Path(self.s_path), delimiter='\t')
        
        self.t = static[0,:]
        self.static = static[1:,:]
        
        self.WL = np.loadtxt(Path(folderpath,'..','Calibration','WavelengthTable.dat'), delimiter='\t')[:,1]
        
        self.signal_strength = signal_strength
        
       
        

    
    # Functions for Raw Data:
        
    z_range = {'very weak': 0.001,
              'weak': 0.005,
              'medium': 0.05,
              'strong': 0.1
              }
        
    def plot(self,signal_strength='weak'):
        """
        In this function some helpful graphs are plotted in a batch to obtain an overview over the raw data.

        """
        z_range = {'very weak': 0.001,
                  'weak': 0.005,
                  'medium': 0.05,
                  'strong': 0.1
                  }
        
        contour(None,None,self.transient,
                zmin=1-z_range[signal_strength],zmax=1+z_range[signal_strength],
                title=f'{Path(self.path).name} transient',xlabel='Datapoint',ylabel='Pixel')
        contour(None,self.WL,self.static,
                zmin=0,zmax=1,
                title=f'{Path(self.path).name} static',xlabel='Datapoint',ylabel='Wavelength/nm')    

    def searchFlip(self,xmin=0,xmax=None,z_range=z_range):
        
        """
        This function helps with finding the phase flip.
        """
        
        try:
            transient=self.transient_fc
        except:
            transient=self.transient
        
        if xmax==None:
            xmax = self.transient.shape[1]
        
        found_point='n'
        while found_point=='n':
            contour(None,None,transient[:,xmin:xmax],
                    zmin=1-z_range[self.signal_strength],zmax=1+z_range[self.signal_strength],
                    title=f'{Path(self.path).name} transient',xlabel='Datapoint',ylabel='Pixel')    
            
            found_point = str(input('found flip? (y/n) '))
            
            if found_point=='y':
                self.flip_position = int(input('position: '))
                self.flip_direction = str(input('direction: '))
                break
            
            xmin = int(input('min position= '))
            xmax = int(input('max position= '))
            


    def findFlip(self):
        """
        This doesn't work yet. It is an attempt to find the flip automatically.
        """

        variance=[]
        for n in range(self.transient.shape[1]-1):
            variance.append(np.nanvar((self.transient[:,n],1/self.transient[:,n+1])))
            
        
    def correctFlip(self,z_range=z_range):
        
        transient_c=self.transient
        
        if self.flip_direction=='before':
            transient_c[:,:self.flip_position]=1/self.transient[:,:self.flip_position]
        if self.flip_direction=='after':
            transient_c[:,self.flip_position:]=1/self.transient[:,self.flip_position:]

        data=np.vstack((self.dt,transient_c))
        
        np.savetxt(Path(Path(self.t_path).parent,str(Path(self.t_path).stem)+'_fc'+Path(self.t_path).suffix), data, delimiter='\t', fmt='%1.8f')
        
        self.transient_fc = transient_c
        
        contour(None,None,self.transient,
                zmin=1-z_range[self.signal_strength],zmax=1+z_range[self.signal_strength],
                title=f'{Path(self.path).name} transient flip corrected',xlabel='Datapoint',ylabel='Pixel') 

        more_flips = input('more flips? (y/n)  ')
        
        if more_flips=='y':
            self.plotFlip()

#%% Execute RawData Functions here:
    
# dt_ma, WL, transient_ma,t_ma, static_ma, t_path = getRawData(Path(folderpath,'05_ma'))   
# transient_c = correctFlip(dt_ma,WL,transient_ma,1144,'before',Path(str(t_path).replace('.dat','')+'_fc.dat')) 

# data={}
# for path in folderpath:
#     data[Path(path).name]=RawData(path)
 
           
#%% Treated Data:

class treatedData:
    """
    get treated data (chirp corrected, averaged)
    """
    def __init__(self,folderpath=None,signal_strength='weak'):
        

        if folderpath==None:
            folderpath = GUI.SelectFolder() 
        
        self.path=folderpath
            
        filelist=glob(str(folderpath)+'/**/*',recursive=True)
        
        if len(filelist)==0:
            logging.error(f'no files found in: {str(Path(folderpath).name)}.')
            sys.exit
        
        for f in filelist:
            if 'cc' in f and 'avg' in f and '.dat' in f:
                data = np.loadtxt(f, delimiter='\t')
                self.TA = data[1:,1:]
                self.dt = data[1:,0]
                self.WL = data[0,1:]
            
            if 'static' in f:
                pass
        
        # if not self.TA:
        #     logging.critical(f'No TA file found for: {str(Path(folderpath).name)}')
                
        self.signal_strength=signal_strength
                
    
    def plot(self,xmin=None,xmax=None,ymin=None,ymax=None):
        """
        In this function some helpful graphs are plotted in a batch to obtain an overview over the raw data.

        """
        z_range = {'very weak': 0.001,
                  'weak': 0.005,
                  'medium': 0.05,
                  'strong': 0.1
                  }
        
        contour(self.WL,None,self.TA,
                xmin=xmin,xmax=xmax,
                ymin=ymin,ymax=ymax,
                zmin=0-z_range[self.signal_strength],zmax=0+z_range[self.signal_strength],
                title=f'{Path((self.path)).name} transient',xlabel='Wavelength/nm',ylabel='dt/ps')
        

#%% Execute Treated Data Functions here:
    
# filelist = [
#             # r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/02_ma',
#             r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/05_ma_rot',
#             # r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/06_ACN_rot',
#             r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/07_parallel_rot',
#             r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/08_perp_rot',
#             r'C:/Users/work/Messdaten/U21_TA/20220422_Berkefeld/12_short',
#             r'C:/Users/work/Messdaten/U21_TA/20220422_Berkefeld/13_long',
#             # r'C:/Users/work/Messdaten/U21_TA/20220422_Berkefeld/14_ACN_long',
#             # r'C:/Users/work/Messdaten/U21_TA/20220422_Berkefeld/15_ACN_short'
#             ]

# data={}
# for f in filelist:
#     try:
#         data[str(Path(f).name)]=treatedData(str(Path(f)))
#     except:
#         print(f'{Path(f).name} not existing.')
        
#%%

# for key in data.keys():
#     try:
#         data[key].plot(xmin=400,xmax=700)
#     except:
#         print(key)
        
    
#%% Remove Spikes:

#%% Calculate


    
#%% Fitted Data:
    
class fitData :
    def __init__(self,folderpath=None):
        
        if folderpath==None:
            folderpath = GUI.SelectFolder() 
        
        self.path=folderpath
        
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
        
        # Get Path to absorption spectrum:
                
        Abspath = glob(str(Path(Path(folderpath).parent,'Absorption','*')))
                
        if len(Abspath)>1:
            for i in Abspath:
                print(i+'\n')
                
        
                # data = np.genfromtxt(Abspath, delimiter=';')
                # self.Abs_WL = data[:,0]
                # self.Abs = data[:,1]
                
        

    def plot(self,GUI=False):
        
                
        plot(self.DAS_WL,self.DAS, 
             label=[str(i)+' ps' for i in self.tau], title=str(Path(self.path).name), 
             xlabel='WL/nm', ylabel=r'$\Delta$OD',
             GUI=GUI
             )
       

    
#%% Execute Treated Data Functions:
# if __name__ == '__main__':    
#     fitdata={}
#     for f in filelist:
#         try:
#             fitdata[str(Path(f).name)]=fitData(str(Path(f)))
#         except:
#             print(f'{Path(f).name} not existing.')