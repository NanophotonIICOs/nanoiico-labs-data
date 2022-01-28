import os
import glob
import sys
from datetime import date
import pandas as pd
import numpy as np
import h5py as h5
from os import walk
from IPython.display import display, clear_output

def extractdata(daypath):
    data = []
    datac=[]
    for name in sorted(glob.glob(daypath+'/*.xls')):
        dat=pd.read_excel(name).values
        datac.append(dat[::-1])

    for name in sorted(glob.glob(daypath+'/*.h5')):
        dat=h5.File(name,'r')
        dset=list(dat.keys())
        datac.append(dat[dset[0]][:,:])
   
    if 'pl' in daypath and not daypath.endswith('cpl'):
        for name in sorted(glob.glob(daypath+'/*.dat')):
            dat=np.loadtxt(name)
            datac.append(dat[:,:])
    
    data.append(datac)
    if data:
        return data
    else: pass


def create_datasets(monthpath,groupobj):
    daysexps = os.listdir(monthpath)
    exptypes = ['ras','rd','pl','pr']
    if daysexps:
        for dayexp in daysexps:
            if any(exptype in dayexp for exptype in exptypes):
                daypath = monthpath
                daypath += '/'+dayexp
                dataextracted = extractdata(daypath)
                #print(len(dataextracted[0][0]))
                maxdimrows = 0
                maxdimcols = 0
                lend = len(dataextracted[0])

                if lend > 0:
                    maxdimrows = max([len(j) for j in dataextracted[0]])
                    maxdimcols = max([dataextracted[0][j].shape[1] for j in range(lend)])
                    npa = np.empty((maxdimrows,maxdimcols,lend))
                    for i in range(lend):
                        rows,cols = dataextracted[0][i].shape
                        npa[0:rows,0:cols,i] = dataextracted[0][i]
                        
                else: pass
                dataset = groupobj.require_dataset(dayexp,shape=npa.shape,data=npa,dtype=np.float64)
    else: 
        print("no files in directory")


def create_newh5groups(path,h5_file,months):
    for new_group in months:
        print(new_group)
        exppath = path
        exppath+='/'+new_group
        group = h5_file.require_group(new_group)
        create_datasets(exppath,group)

def create_newh5(sample,system):
    masterpath="/media/labfiles/lab-exps/spectro-lab"
    path_h5="/media/labfiles/lab-exps/exp-h5-files/spectro-lab"
    path_h5+='/'+system+'/'+sample
    masterpath+='/'+system+'/'+sample
    print(masterpath)
    new_file = h5.File(path_h5+'.h5','a')
    months = os.listdir(masterpath)
    if months:
        create_newh5groups(masterpath,new_file,months)
        print("New h5 file created for ",sample)
        new_file.close()
    else: 
        print("no month folders")
        new_file.close()
    
    
changed_path = sys.argv[1]
partspath = changed_path.split(os.sep)
samplename = partspath[-4]
system = partspath[-5]
print(samplename,system)
create_newh5(samplename,system)
