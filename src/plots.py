__author__ = 'O. Ruiz-Cigarrillo'
import os
import glob
from tabulate import tabulate
from datetime import date
import pandas as pd
import numpy as np
import h5py as h5
from os import walk
from IPython.display import display, clear_output
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit
from scipy.signal import savgol_filter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes



def join_labels(string,extra=r""):
    str_day=string.split('/')[-2].split('-')[0:4]
    str_exp=string.split('/')[-1].split('.')[0]
    exp_label='-'.join(str_day)+' ---'+str_exp+' '+extra
    return exp_label  

class parameters():
    def __init__(self,**kwargs):
        # setting any extra parameters provided with initialisation
        for key,value in kwargs.items():
            setattr(self,key,value)

class AttrDict(dict):
    """turns a dictionary into an object with attribute style lookups"""
    def __init__(self, *args, **kwargs):
        super(AttrDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class figs(parameters):
    def __init__(self,inputfile,sample):
        if type(inputfile)==dict:
            inputfile=AttrDict(inputfile) 

        self.data=sample.data
        self.expi=inputfile.expi
        self.expf=inputfile.expf
        self.lendata=len(sample.data)
        self.filesname=sample.filesname



    def plotras(self):
        # if self.expi =='none' or self.expf=='none':
        #     self.expi=0
        #     self.expf=self.lendata
        # elif self.expi >self.expf:
        #     Warning("The final experiment should be major to the initial experiment!")
        #     self.expf = len(self.data)
        fig,ax = plt.subplots(nrows=1,ncols=2,figsize=(10,6))
        plt.subplots_adjust(wspace=0.25)
        for i in range(self.expi,self.expf):
            for j in range(len(self.data[i])):
                lbl=join_labels(self.filesname[i][j]) if i>0 else join_labels(self.filesname[i][j])
                ax[0].plot(self.data[i][j][:,0],self.data[i][j][:,1],label=lbl)

                r0=self.data[i][j][:,2]
                bgr=savgol_filter(r0, 41, 2) 
                r1  = (r0-bgr)
                
                axins1 = inset_axes(ax[1], width="100%", height="100%",
                            bbox_to_anchor=(0.0,0.7,0.5,0.3),
                            bbox_transform=ax[1].transAxes,
                            borderpad=0,
                                )
                
                axins1.set_xticks([])
                axins1.set_yticks([])
                axins1.plot(self.data[i][j][:,0],r0)
                axins1.plot(self.data[i][j][:,0],bgr,'r')
                #axins1.set_xlim([1.47,1.53])
                #axins1.set_ylim([-3e-3,0.3e-3])
                ax[1].plot(self.data[i][j][:,0],r1)

        ax[0].set_xlabel("Photon energy (eV)")    
        ax[0].set_ylabel("RAS")    
        ax[1].set_xlabel("Photon energy (eV)")    
        ax[1].set_ylabel("R")    
        ax[0].legend(frameon=False,fontsize=10)        
        plt.show()        




# def CorrImag(datIm,grade,offset):
#     ImRes=np.zeros(datIm.shape)
#     for i in range(ImRes.shape[0]):
#         datnum=np.array(datIm[i,:])
    
#         x=np.arange(0,datnum.size)
#         a,b =np.polyfit(x,datnum,grade)
#         fit=a*x+b
#         ImRes[i,:]=fit-datnum+offset
#     return ImRes