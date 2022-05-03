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

path=GUI.SelectFile()

data2= np.loadtxt(Path(path))

#%%

contour(data2[0,1:],None,data2[1:,1:],zmin=-0.001,zmax=0.001)
# contour(None,None,data2[1:,1:],zmin=0.99,zmax=1.01)

#%%

# write=data2

# TA=write[1:,1:]

# TA[TA<-0.1]=np.nan
# TA[TA>0.1]=np.nan

# write[1:,1:]=TA

WL=np.insert(data2[0,1:],0,0)

write=data2

write[1:,1:]=data2[1:,1:]*(-1)
 
#%%

contour(None,None,write[1:,1:],zmin=-0.01,zmax=0.01)
# contour(None,None,write[1:,1:],zmin=0.99,zmax=1.01)

#%%

np.savetxt(path, write, delimiter='\t', fmt='%1.8f')
