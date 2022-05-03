# -*- coding: utf-8 -*-
"""
This is a function to make nice figures with minimum effort.
"""
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable
import sys

from pathlib import Path


import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        #logging.FileHandler("Logging.log"),
        logging.StreamHandler(sys.stdout)
    ])


#%%

def MLplot( x,
            Y,
            xrange=None,
            linestyles=None,
            colors=None,
            padx=0.04,
            yrange=(None,None),
            pady=0.1,
            title=None,
            label=[],
            xlabel=None,
            ylabel=None,
            xrule=False,
            xscale='linear',
            scale_break=None,
            GUI=False,
            dpi=1700
            ):
    
    if GUI:
        matplotlib.use('TkAgg')

    # this function wants to deal with lists   

    if type(Y)!=list:
        Y=[Y]
    
    if linestyles==None or len(linestyles)!=len(Y):
        linestyles=['-']*len(Y)
        
    if colors==None or len(colors)!=len(Y):
        colors=[None]*len(Y)
    
    # if no x-values are provided, make some:
        
    if type(x).__module__ != np.__name__:
        x=np.arange(0,Y[0].shape[0],1)

    #plot data
        
    fig=plt.figure(dpi=dpi)

    for n,y in enumerate(Y):
        if type(y)==tuple: #if you have data with different x-scales, you need to specify the dataset as (x,y) touple.
            if xrange:
                x0=y[0][np.argmax(y[0]>xrange[0]):np.argmax(y[0]>xrange[1])]
                y0=y[1][np.argmax(y[0]>xrange[0]):np.argmax(y[0]>xrange[1])]
            else:
                x0=y[0]
                y0=y[1]
        else:
            if xrange:
                x0=x[np.argmax(x>xrange[0]):np.argmax(x>xrange[1])]
                y0=y[np.argmax(x>xrange[0]):np.argmax(x>xrange[1])]
            else:
                x0=x
                y0=y
        if linestyles[n]=='o':
            plt.plot(x0,y0,'o',markersize=0.5,color=colors[n])
        else:
            plt.plot(x0,y0,linestyle=linestyles[n],color=colors[n])
            
    
    #Axis stuff:

    ax=plt.gca()
    ax.set_ylim(bottom=yrange[0])
    ax.set_ylim(top=yrange[1])
    ax.margins(padx,pady)
    ax.set_xscale(xscale)
    if xscale=='symlog':
        if scale_break:
            plt.xscale('symlog',linthresh=scale_break)
            ax=plt.gca()
            ticks_lin=np.append(np.linspace(np.nanmin(x),0,2),np.linspace(0,scale_break,5))
            ticks_label_lin=[str(round(x,1)) for x in ticks_lin]
            ticks_log=[x for x in np.exp(np.linspace(np.log(scale_break),np.nanmax(np.log(x)),8))]
            ticks_log.pop(0)
            ticks_label_log=[str(round(x)) for x in ticks_log]
            
            ticks=np.append(ticks_lin,ticks_log)
            ticks_label=ticks_label_lin+ticks_label_log
            
            plt.axvline(x=scale_break,color='k',linestyle='--',linewidth=0.5)

            plt.xticks(ticks,labels=ticks_label)
        else:
            logging.error('Please specify the scale break for semi log. scale.')
            
            
    
    #And some layout adjustment:
    if xrule:
        plt.axhline(y=0, color='k', linewidth=1)   

    plt.title(title)
    
    if len(label)==0:
         for n in range(len(Y)):
             label.append('Curve'+str(n+1))       
    plt.legend(label)#,bbox_to_anchor=(1,1))
    
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
        
    plt.tick_params(axis='x', direction='in')
    plt.tick_params(axis='y', direction='in')
    
    plt.tight_layout()

    
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