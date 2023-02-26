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
        
    def get_peaks(self):
        self.x = self.exp[:,0]
        self.y = self.exp[:,1]
        self.peaks_results = namedtuple("peaks_result",["xind","yind"])
        indexes = peakutils.indexes(self.y, thres=0.5, min_dist=30)
        xind = self.x[indexes]
        yind = self.y[indexes]
        return self.peaks_results(xind,yind)
        

        
        