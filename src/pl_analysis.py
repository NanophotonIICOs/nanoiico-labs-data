import numpy as np
import peakutils
from peakutils.plot import plot as pplot
import matplotlib.pyplot as plt
from typing import Dict
from collections import namedtuple


class pl:
    def __init__(self,exp,**kwargs):
        self.exp = exp
        self.parameters = kwargs
        self.x = None
        self.y = None
        self.indexes = None
        
        
    def get_peaks(self,min_dist=30,thres=0.5):
        self.x = self.exp[:,0]
        self.y = self.exp[:,1]
        self.peaks_results = namedtuple("peaks_result",["xind","yind"])
        self.indexes = peakutils.indexes(self.y, thres=thres, min_dist=min_dist)
        xind = self.x[self.indexes]
        yind = self.y[self.indexes]
        return self.peaks_results(xind,yind)
    
    def plot_peaks(self):
        fig,ax= plt.subplots(figsize=(7,8))
        ax.plot(self.x,self.y,'-b',lw=1)
        ax.plot(self.x[self.indexes], self.y[self.indexes],'x',color='red')
        return fig

    
        