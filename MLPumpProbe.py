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
import matplotlib.pyplot as plt

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
    
filelist = [
            # r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/02_ma',
            r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/05_ma_rot',
            # r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/06_ACN_rot',
            r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/07_parallel_rot',
            r'C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/08_perp_rot',
            r'C:/Users/work/Messdaten/U21_TA/20220422_Berkefeld/12_short',
            r'C:/Users/work/Messdaten/U21_TA/20220422_Berkefeld/13_long',
            # r'C:/Users/work/Messdaten/U21_TA/20220422_Berkefeld/14_ACN_long',
            r'C:/Users/work/Messdaten/U21_TA/20220422_Berkefeld/15_ACN_short'
            ]

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
    """
    Class to quickly get fitted Data and Plot nice figures.
    """
    
    def __init__(self,folderpath=None,Abspath=None):
        
        if folderpath==None:
            folderpath = GUI.SelectFolder() 
            
        if not Path(folderpath).is_dir():
            logging.error(f'Path "{folderpath}" does not exist.')
            sys.exit()
            
        
        self.path=folderpath
        self.title=Path(folderpath).name
        
        self.Abspath=Abspath
 
        self.getInfo()
               
        #Initialize
        self.No_Comp=0
        self.tau=[]
        self.DAS = []
        self.path = folderpath
        

        self.getParms()
        self.getData()
        

        
                
    ##Functions####################
    
    
    def getInfo(self):
        
        try:
            info=Path(self.path,'info.txt').read_text().split('\n')
            self.info={}
            for line in info:
                if len(line)>1:
                    c=line.split('=')
                    self.info[c[0]]=c[1]
            
            self.title=f'{self.info["Sample"]}, Pol.: {self.info["Polarization"]}, \u0394t: {self.info["Timerange"]}'
        except:
            logging.critical(f'no info found in {Path(self.path,"info.txt")}')
            
            
        
    def getParms(self):
        
        files = glob(str(self.path)+'/**/*', recursive=True)
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
    
                            
    
    def getData(self):
        
        # WLTablepath = glob(str(Path(Path(self.path).parent,'Calibration/*WaveLengthTable*')),recursive=True)[0]
        # self.WavelengthTable = np.loadtxt(WLTablepath,delimiter='\t')
        
        files = glob(str(self.path)+'/**/*', recursive=True)        
        for f in files:
           
            if 'amplitudes' in f:
                data = np.genfromtxt(Path(f), delimiter='\t',skip_header=4)
                self.DAS_WL = data[:,0]
                
                
                for n in range(self.No_Comp):
                    self.DAS.append(data[:,n+1])

            if '.fit' in f:
                data = np.genfromtxt(Path(f), delimiter='\t',)
                self.fit = data[1:,1:].T
                self.fit_WL = data[1:,0]
                self.fit_dt = data[0,1:]
    
            elif '.dat' in f and 'cc' in f:
                data = np.genfromtxt(f)
                self.WL = data[0,1:]
                self.dt = data[1:,0]
                self.TA = data[1:,1:]
            
            elif 'static' in f:
                data = np.genfromtxt(f)
                self.static = -np.log10(data[1:,:])
                self.static_t = data[0,:]
        
        # Get Path to absorption spectrum:
        if self.Abspath==None:        
            self.Abspath = glob(str(Path(Path(self.path).parent,'Absorption','*')))
                    
            if len(self.Abspath)>1:
                self.Abspath=GUI.SelectFile(title='Specify Path to absorbance spectrum',
                                       path=Path(self.path).parent)
            
        Abs = np.genfromtxt(self.Abspath,delimiter=';')
        self.Abs_WL = Abs[:,0]
        self.Abs = Abs[:,1]
        

            

    def plot(self,
             DAS=True, ROI=None,
             Dec_ROI=None, scale_break=None,
             Abs=True,Abs_ROI=None,
             save=False,
             gui=False,
             dpi=2000):
        
        if save:
            Path(self.path,'Figures').mkdir(exist_ok=True)
        
        if DAS:
            # try:
                fig=plot(self.DAS_WL,self.DAS, 
                    label=[str(i)+' ps' for i in self.tau], 
                    title=self.title, 
                    xlabel='WL/nm', ylabel=r'$\Delta$OD',
                    GUI=gui,
                    xrule=True,
                    dpi=dpi
                    )
                if save:
                    fig.savefig(Path(self.path,'Figures','DAS'),dpi='figure', bbox_inches = "tight")
                    plt.close()
                    
            # except:
            #     logging.warning(f'no DAS available for {self.title}')
        

        if Dec_ROI:
            Y=[]
            label=[]
            colors_list=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
            colors=[]
            linestyles=[]
            for n,i in enumerate(Dec_ROI):
                fromx=np.argmax(self.WL>i[0])
                tox=np.argmax(self.WL>i[1])
                Y.append(np.mean(self.TA[:,fromx:tox],axis=1))
                linestyles.append('o')
                colors.append(colors_list[n])
                label.append(f'TA from {i[0]}nm to {i[1]}nm')
                fromx=np.argmax(self.fit_WL>i[0])
                tox=np.argmax(self.fit_WL>i[1])
                Y.append(np.mean(self.fit[:,fromx:tox],axis=1))
                linestyles.append('-')
                colors.append(colors_list[n])
                label.append('_nolegend_')
            
            if not scale_break:
                scale_break = round(np.mean(self.tau)/2)
                
            fig=plot(self.dt, Y,
                 xlabel='dt/ps', ylabel=r'$\Delta$OD',
                 title=self.title,
                 colors=colors,
                 linestyles=linestyles,
                 label=label,
                 xscale='symlog',
                 scale_break=scale_break,
                 xrule=True,
                 dpi=dpi)
            if save:
                fig.savefig(Path(self.path,'Figures','Decay'),dpi='figure', bbox_inches = "tight")
                plt.close()
        
        
        if Abs:
            # try:
                fig=plot(self.WL,[np.mean(self.static,axis=1),
                     (self.Abs_WL,self.Abs)],
                     xrange=ROI,                     
                     xlabel='WL/nm', ylabel='Abs./OD',
                     title=self.title,
                     label=['Abs. from pump probe','Absorbance'],
                     xrule=True,
                     dpi=dpi)
                if save:
                    fig.savefig(Path(self.path,'Figures','Abs'),dpi='figure', bbox_inches = "tight")
                    plt.close()
                    
                if Abs_ROI:
                    Y=[]
                    label=[]
                    for i in Abs_ROI:
                        fromx=np.argmax(self.WL>i[0])
                        tox=np.argmax(self.WL>i[1])
                        Y.append(np.mean(self.static[fromx:tox,:],axis=0))
                        label.append(f'Abs. from {i[0]}nm to {i[1]}nm')
                        
                    fig=plot(self.static_t/60, Y,
                             xlabel='t/min', ylabel='OD',
                             yrange=(0,None),
                             title=self.title, 
                             label=label,
                             xrule=True,
                             dpi=dpi)
                    if save:
                        fig.savefig(Path(self.path,'Figures','Degradation'),dpi='figure', bbox_inches = "tight")
                        plt.close()
                else:
                    pass
                    
            # except:
            #     logging.warning(f'no Absorbancespectra available for {self.title}')
                

    
#%% Execute Treated Data Functions:
if __name__ == '__main__':    
    fitdata={}
    for f in filelist:
        try:
            Abspath="C:/Users/work/Messdaten/U21_TA/20220421_Berkefeld/Absorption/02_Co_Otf_ACN_1mm_c2.csv"
            fitdata[str(Path(f).name)]=fitData(str(Path(f)),Abspath)

        except:
            print(f'{Path(f).name} not existing.')
            
    for key in fitdata.keys():
        ROI=(400,700)
        Dec_ROI=[(445,455),(550,600)]
        Abs_ROI=[(400,450)]
        fitdata[key].plot(ROI=ROI,Dec_ROI=Dec_ROI,Abs_ROI=Abs_ROI,save=True)
