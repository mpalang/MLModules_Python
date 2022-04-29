# -*- coding: utf-8 -*-
"""
This is a function to make nice figures with minimum effort.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable

from pathlib import Path

#%%

def MLplot( x,
            Y,
            xmin=None,
            xmax=None,
            ymin=None,
            ymax=None,
            title=None,
            label=[],
            xlabel=None,
            ylabel=None,
            GUI=False
            ):
    
    if GUI:
        matplotlib.use('TkAgg')
    
    #padding in percent of maximum
    
    padx = 1
    pady = 1

    # this function wants to deal with lists   

    if type(Y)!=list:
        Y=[Y]
        
    if type(x).__module__ != np.__name__:
        x=np.arange(0,Y[0].shape[0],1)

    # Make separate figures for each dataset in list:
        
    fig=plt.figure()
    
    plt.tick_params(axis='x', direction='in')
    plt.tick_params(axis='y', direction='in')
    
    # set x-Range if not specified. You can change the padding here.
    
    if xmin==None:
        xmin = np.nanmin(x[x!=-np.inf])*(1-padx/100)
    if xmax==None:
        xmax = np.nanmax(x[x!=np.inf])*(1+padx/100)
    
    plt.xlim([xmin,xmax])


    for n,y in enumerate(Y):
        if type(y)==tuple:
            plt.plot(y[0],y[1])
        else:
            plt.plot(x,y)
    
        
        
    plt.title(title)
    
    if len(label)==0:
         for n in range(len(Y)):
             label.append('Curve'+str(n+1))       
    plt.legend(label)#,bbox_to_anchor=(1,1))
    
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    
    return fig
    
        

def MLcontour(x,
             y,
             Z,
             xmin=None,
             xmax=None,
             ymin=None,
             ymax=None,
             zmin=None,
             zmax=None,
             separate=True,
             title=None,
             xlabel=None,
             ylabel=None
             ):
    
    if type(x).__module__ != np.__name__:
        x=np.arange(0,Z.shape[1],1)
        
    if type(y).__module__ != np.__name__:
        y=np.arange(0,Z.shape[0],1)
    
    
    if zmin==None:
        zmin=np.nanmin(Z[Z!=-np.inf])
        
    if zmax==None:
        zmax=np.nanmax(Z[Z!=np.inf])
   
    fld=np.random.rand(10,10)*100    
    levels=20
    
    levels = np.linspace(zmin,zmax,levels+1)
    
    img=plt.contourf(x,y,Z,levels=levels,cmap='rainbow')
    plt.xlim(xmin,xmax)
    plt.ylim(ymin,ymax)
    
    
    plt.colorbar(img)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)

    plt.tick_params(axis='x', direction='in')
    plt.tick_params(axis='y', direction='in')
    
    plt.show() 
        
def test():
    print('hello')