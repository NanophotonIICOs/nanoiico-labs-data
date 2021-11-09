import os
import glob
from tabulate import tabulate
from datetime import date
import pandas as pd
from os import walk
from IPython.display import display, clear_output


class experiments:
    def __init__(self,path,exptype):
        self.path=path
        self.data=[]
        self.foldername=[]
        self.pathname=[]
        self.filesname=[]
        self.count = 0
        self.ptable=[]
        self.headers=['No. Dir','Name Dir', 'No. files']
        self.datac=[]
        #self.namef=[]
        if exptype==None:
            self.exptype = 'ras'
        else:
            self.exptype=exptype
        
        for (dirpath, dirnames, filenames) in walk(self.path):
            self.foldername.append(dirpath)
        
        self.foldername = sorted(self.foldername)
        for dirpath in self.foldername:
            clear_output(wait=True)
            if self.exptype in dirpath:
                self.datac=[]
                self.namef=[]
                for name in sorted(glob.glob(dirpath+'/*.xls')):
                    if exptype in name:
                        #print(name.split('/media/labfiles/ruco/experiments')[1]) 
                        dat=pd.read_excel(name).values
                        self.datac.append(dat[::-1])
                        self.namef.append(name)
                self.data.append(self.datac)
                self.filesname.append(self.namef)
                self.pathname.append(dirpath)
                self.ptable.append([self.count,dirpath.split('/media/labfiles/lab-experiments/spectroscopy-lab/cryogenic-system-1/')[1],len(self.datac)])
                print(tabulate(self.ptable,self.headers,tablefmt="github",colalign=("center","left","center")))
                self.count+=1
        print(tabulate(self.ptable,self.headers,tablefmt="github",colalign=("center","left","center")))
        

