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

class experiments:
    def __init__(self, lab, sys, exptype, sample):
        self.path='/media/labfiles/lab-exps'
        self.headers=['No. Dir','Name Dir', 'No. files']
        self.count=0
        self.foldername=[]
        self.filesname=[]
        self.pathname=[]
        self.ptable=[]
        self.datac=[]
        self.data=[]
        self.exptype=exptype

        self.path=self.path+'/spectro-lab' if lab==1 else self.path+'/ellipsometry-lab'
        if lab==2:
            self.path=self.path+'/nano' if sys=='nano' else self.path+'/cry-sys-2' if sys=='cry2' else self.path+'/cry-sys-1' if sys=='cry1' else self.path
    
        for (dirpath, dirnames, filenames) in walk(self.path):
            if sample in dirpath:
                self.foldername.append(dirpath)

        self.foldername = sorted(self.foldername)
        for dirpath in self.foldername:
            clear_output(wait=True)
            if self.exptype in dirpath:
                self.datac=[]
                self.namef=[]
                for name in sorted(glob.glob(dirpath+'/*.xls')):
                    if exptype in name:
                        dat=pd.read_excel(name).values
                        self.datac.append(dat[::-1])
                        self.namef.append(name)
                for name in sorted(glob.glob(dirpath+'/*.h5')):
                    if exptype in name:
                        dat=h5.File(name,'r')
                        dset=list(dat.keys())
                        self.datac.append(dat[dset[0]][:,:])
                        self.namef.append(name)
                for name in sorted(glob.glob(dirpath+'/*.dat')):
                    if exptype in name:
                        dat=np.loadtxt(name)
                        self.datac.append(dat[:,:])
                        self.namef.append(name)
                self.data.append(self.datac)
                self.filesname.append(self.namef)
                self.pathname.append(dirpath)
                self.ptable.append([self.count,dirpath.split(self.path+'/')[1],len(self.datac)])
                self.count+=1
        
        if self.datac:
            print(tabulate(self.ptable,self.headers,tablefmt="github",colalign=("center","left","center")))
        else:
            print("no experiments found, change search parameters")
  
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



class plots(parameters):
    def __init__(self,inputfile):
        if type(inputfile)==dict:
            inputfile=AttrDict(inputfile) 
        for i in inputfile:
            print(i)