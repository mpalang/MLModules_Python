# -*- coding: utf-8 -*-
"""
This is a function to make nice figures with minimum effort.
"""
import numpy as np
import matplotlib.pyplot as plt

#%%

def FigureML(x,
             Y,
             xmin=None,
             xmax=None,
             ymin=None,
             ymax=None,
             separate=True
             ):
    
################################################################################################################################################################################

    # this function wants to deal with lists   

    if type(Y)!=list:
        Y=[Y]
    
    # Make separate figures for each dataset in list:
        
    if separate:
    
        for y in Y:
                
            if type(x)!=np.array:
                x=np.arange(0,len(y),1)
        
            fig = plt.figure() 
            
            plt.tick_params(axis='x', direction='in')
            plt.tick_params(axis='y', direction='in')
            
            # if xmin or xmax or ymin or ymax:
            #     ax.set_xlim(xmin,xmax)
            #     ax.set_ylim(ymin,ymax)
            
            plt.plot(x,y)
            
            
    
    return None


x=np.arange(0,10,0.1)

y=np.sin(x)

FigureML(x,y)