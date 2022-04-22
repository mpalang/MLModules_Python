# -*- coding: utf-8 -*-
"""
This is a function to make nice figures with minimum effort.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable

#%%

def MLplot(x,
             Y,
             xmin=None,
             xmax=None,
             ymin=None,
             ymax=None,
             separate=True,
             title=None,
             label=None,
             xlabel=None,
             ylabel=None,
             Abs=False,
             static=False,
             show=True
             ):
    
    
    #padding in percent of maximum
    
    padx = 1
    pady = 1

    # this function wants to deal with lists   

    if type(Y)!=list:
        Y=[Y]
        
    if type(x).__module__ != np.__name__:
        x=np.arange(0,Y[0].shape[0],1)

    # Make separate figures for each dataset in list:
    
    plt.tick_params(axis='x', direction='in')
    plt.tick_params(axis='y', direction='in')
    
    # set x-Range if not specified. You can change the padding here.
    
    if xmin==None:
        xmin = np.nanmin(x[x!=-np.inf])*(1-padx/100)
    if xmax==None:
        xmax = np.nanmax(x[x!=np.inf])*(1+padx/100)
    
    plt.xlim([xmin,xmax])
    
        
    if separate:
    
        for y in Y:
            
            # set y-Range if not specified:
            
            if ymin==None:
                ymin=np.nanmin(y[y!=-np.inf])*(1+pady/100)
            if ymax==None:
                ymax=np.nanmax(y[y!=np.inf])*(1+padx/100)
            
            plt.ylim([ymin,ymax])
            
            # Legend, labels etc.:
                
            plt.title(title)
            plt.legend(bbox_to_anchor=(1,1))
            
            #plot:
                
            plt.plot(x,y,label=label)
            
            plt.show()
            
    else:
        for n,y in enumerate(Y):
            fig=plt.plot(x,y)
        
        if Abs:
            factor=np.nanmax(Y)/np.nanmax(Abs[1][Abs[1]!=np.inf])
            fig=plt.plot(Abs[0],Abs[1]*factor,'k',linestyle='dashed',linewidth=0.5)
            label.append('Absorbance')
            
        if static:
            statAbs=-np.log10(static[1])
            factor=np.nanmax(Y)/np.nanmax(statAbs[statAbs!=np.inf])
            fig=plt.plot(static[0],statAbs*factor,'r',linestyle='dotted',linewidth=0.5)
            label.append('Abs. from TA')
            
            
        plt.title(title)
        plt.legend(label)#,bbox_to_anchor=(1,1))
        
        plt.ylabel(ylabel)
        plt.xlabel(xlabel)
        
        if show:
            plt.show()
        else:   
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
             title=None
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
    plt.colorbar(img)
    plt.title(title)

    plt.tick_params(axis='x', direction='in')
    plt.tick_params(axis='y', direction='in')
    
    plt.show() 
        
def test():
    print('hello')