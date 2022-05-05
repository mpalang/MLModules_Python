# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 09:29:24 2022

@author: work
"""
from pathlib import Path
import os

import numpy as np
import MLModules.MLBasic_GUI as GUI


from MLModules.MLPlot import MLplot as plot
from MLModules.MLPlot import MLcontour as contour

#%%

path1="Z:/Nutzer/Lang/privat/02_Projekte/Cobalt_Berkefeld_Tübingen/Messdaten/Re _TA_Messungen/CoOTf.csv"
path2="Z:/Nutzer/Lang/privat/02_Projekte/Cobalt_Berkefeld_Tübingen/Messdaten/Re _TA_Messungen/CoOTf_Dikation.csv"
path3="Z:/Nutzer/Lang/privat/02_Projekte/Cobalt_Berkefeld_Tübingen/Messdaten/Re _TA_Messungen/CoOTf_Radikalanion.csv"

#%%


g= np.genfromtxt(Path(path1),delimiter=';')
m=np.genfromtxt(Path(path2),delimiter=';')
a=np.genfromtxt(Path(path3),delimiter=';')

#%%
WL=m[:,0]
a=a[1:,1]
g=g[1:,1]
m=m[:,1]

#%%
# dpi=200
# plot(WL,[g,m,a],label=['groundstate','Ligand-Radikalanion','oxidierte Verbindung, Co-zentriert'],xrule=True,dpi=dpi)
# plot(WL,m-g,label=['TA-Ligand-Radikalanion'],xrule=True,dpi=dpi)
# plot(WL,a-g,label=['TA-oxidierte Verbindung'],xrule=True,dpi=dpi)
# plot(WL,a+m-g,label=['TA-beide'],xrule=True,dpi=dpi)

# contour(data2[0,1:],None,data2[1:,1:],zmin=-0.001,zmax=0.001)
# contour(None,None,data2[1:,1:],zmin=0.99,zmax=1.01)

#%%

import MLModules.MLPumpProbe as pp

filepath= 'E:/Moritz/Messdaten/U21_TA/20220421_Berkefeld/'
Abspath='E:/Moritz/Messdaten/U21_TA/20220421_Berkefeld/Absorption/Co_Abs.dat'

ma2=pp.fitData(filepath+'05_ma_rot',Abspath)

#%%
dpi=200
s=0.04
plot(WL,[((m+a)/1-g)*s]+[(ma2.DAS_WL,i) for i in ma2.DAS],label=['TA-beide','DAS1','DAS2','DAS3'],xrule=True,dpi=dpi,
     xrange=(430,680),yrange=(-0.01,0.02))

# write=data2

# TA=write[1:,1:]

# TA[TA<-0.1]=np.nan
# TA[TA>0.1]=np.nan

# write[1:,1:]=TA

# WL=np.insert(data2[0,1:],0,0)

# write=data2

# write[1:,1:]=data2[1:,1:]*(-1)
 
#%%

# contour(None,None,write[1:,1:],zmin=-0.01,zmax=0.01)
# contour(None,None,write[1:,1:],zmin=0.99,zmax=1.01)

#%%

# np.savetxt(path, write, delimiter='\t', fmt='%1.8f')
