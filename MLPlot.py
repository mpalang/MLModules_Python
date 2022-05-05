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
            label=[],
            title=None,
            xlabel=None,
            ylabel=None,
            xrange=None,
            yrange=(None,None),
            linestyles=None,
            colors=None,
            padx=0.04,
            pady=0.1,
            xrule=False,
            xscale='linear',
            scale_break=None,
            gui=False,
            dpi=200
            ):
    
    """
    Input:
        x: x-values for x-axis
        Y: list of y-values. If x-values differ from 'x', data has to be inserted as touple (x2,y2).
        label: List of curve-labels.
        title: title of plot,
        xlabel: x-axis label.
        ylabel: y-axis label.
        xrange: x-range for plotting as touple (left,right).
        yrange: y-range for plotting as touple (lower,upper)
        linestyles: list with linestyles 'o' for scatter plot. Length has to be same as Y.
        colors: list with colors. Length has to be same as Y.
        padx: white space around data in x-direction.
        pady: white space around data in y-direction.
        xrule: horizontal line at y=0.
        xscale: x-scale. options: 'linear', 'log', 'symlog'
        scale_break: has to be specified for 'symlog'. Determines where to switch from linear to log.
        gui: Graphical user interface.
        dpi: resolution for figures. ~200 for quick view, ~2000 for final images.
        
    Output:
        figure instance from pyplot
        if save option is True, plots are saved in Figure folder in base path.
    
    """
    
    if gui:
        matplotlib.use('TkAgg')

    # this function wants to deal with lists   

    if type(Y)!=list:
        Y=[Y]
    
    if linestyles==None or len(linestyles)!=len(Y):
        linestyles=[None]*len(Y)
        
    if colors==None or len(colors)!=len(Y):
        colors=[None]*len(Y)
    
    # if no x-values are provided, make some:
        
    if type(x).__module__ != np.__name__:
        if type(Y[0])==tuple:
            x=np.arange(0,Y[0][0].shape[0],1)
        else:
            x=np.arange(0,Y[0].shape[0],1)

    #plot data
        
    fig=plt.figure(dpi=dpi)

    for n,y in enumerate(Y):
        if type(y)==tuple: #if you have data with different x-scales, you need to specify the dataset as (x,y) touple.
            if xrange:
                fromx=np.argmax(y[0]>xrange[0])
                tox=np.argmax(y[0]>xrange[1])
                if tox==0:
                    tox=len(y[0])  
                x0=y[0][fromx:tox]
                y0=y[1][fromx:tox]
            else:
                x0=y[0]
                y0=y[1]
        else:
            if xrange:
                fromx=np.argmax(x>xrange[0])
                tox=np.argmax(x>xrange[1])
                if tox==0:
                    tox=len(x)   
                x0=x[fromx:tox]
                y0=y[fromx:tox]
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
            if not xrange:
                xrange=(np.nanmin(x),np.nanmax(x))
            plt.xscale('symlog',linthresh=scale_break)
            ax=plt.gca()
            ticks_lin=np.append(np.arange(xrange[0],0,(scale_break/4)),np.linspace(0,scale_break,5))
            ticks_label_lin=[str(round(x,1)) for x in ticks_lin]
            ticks_log=[x for x in np.exp(np.linspace(np.log(scale_break),np.log(xrange[1]),8))]
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
             ylabel=None,
             dpi=100
             ):
    """

    Parameters
    ----------
    x : TYPE
        DESCRIPTION.
    y : TYPE
        DESCRIPTION.
    Z : TYPE
        DESCRIPTION.
    xmin : TYPE, optional
        DESCRIPTION. The default is None.
    xmax : TYPE, optional
        DESCRIPTION. The default is None.
    ymin : TYPE, optional
        DESCRIPTION. The default is None.
    ymax : TYPE, optional
        DESCRIPTION. The default is None.
    zmin : TYPE, optional
        DESCRIPTION. The default is None.
    zmax : TYPE, optional
        DESCRIPTION. The default is None.
    separate : TYPE, optional
        DESCRIPTION. The default is True.
    title : TYPE, optional
        DESCRIPTION. The default is None.
    xlabel : TYPE, optional
        DESCRIPTION. The default is None.
    ylabel : TYPE, optional
        DESCRIPTION. The default is None.
    dpi : TYPE, optional
        DESCRIPTION. The default is None.

    Returns
    -------
    fig

    """
    
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
    
    fig=plt.figure(dpi=dpi)
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
    return fig
        
def test():
    print('hello')