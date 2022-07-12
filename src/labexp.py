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
        self.raspos1=[]
        self.raspos2=[]
        self.nameraspos1=[]
        self.nameraspos2=[]
        self.nameraspos=[]
        self.exptype=exptype
        self.rasp1table=[]
        self.rasp2table=[]

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
                self.npos1=[]
                self.npos2=[]
                for name in sorted(glob.glob(dirpath+'/*.xls')):
                    singlename=name.split('/')[-1]
                    if exptype in singlename or "RD" in singlename or "rds" in singlename:
                        dat=pd.read_excel(name).values
                        self.datac.append(dat[::-1])
                        self.namef.append(name)
                        if 'pos1' in name or 'Pos1' in name or 'p1' in name:
                            self.raspos1.append(dat[::-1])
                            self.nameraspos1.append(name)
                            self.npos1.append(name)
                        elif 'pos2' in name or 'Pos2' in name or 'p2' in name:
                            self.raspos2.append(dat[::-1])
                            self.nameraspos2.append(name)
                            self.npos2.append(name)
                    else:
                        pass
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

                if self.npos1:
                    self.nameraspos.append(self.npos1)
                elif self.npos2:
                    self.nameraspos.append(self.npos2)

                self.ptable.append([self.count,dirpath.split(self.path+'/')[1],len(self.datac)])
                self.count+=1
                
        if self.datac:
            print(tabulate(self.ptable,self.headers,tablefmt="github",colalign=("center","left","center")))
        else:
            print("no experiments found, change search parameters")
  
    def darray(self):
        alldata=self.data
        
        # maxrowspos1 = max(i.shape[0] for i in self.raspos1)
        # maxcolspos1 = max(i.shape[1] for i in self.raspos1)
        # maxrowspos2 = max(i.shape[0] for i in self.raspos2)
        # maxcolspos2 = max(i.shape[1] for i in self.raspos2)

      

        # #create total array
        # self.araspos1=np.zeros((maxrowspos1,maxcolspos1,len(self.raspos1)))
        # for k in range(len(self.raspos1)):
        #     for i in range(self.raspos1[k].shape[1]):
        #         for j in range(self.raspos1[k].shape[0]):
        #             self.araspos1[j,i,k]=self.raspos1[k][j][i]

        # self.araspos2=np.zeros((maxrowspos2,maxcolspos2,len(self.raspos2)))
        # for k in range(len(self.raspos2)):
        #     for i in range(self.raspos2[k].shape[1]):
        #         for j in range(self.raspos2[k].shape[0]):
        #             self.araspos2[j,i,k]=self.raspos2[k][j][i]

