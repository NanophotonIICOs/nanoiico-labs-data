__author__ = 'O. Ruiz-Cigarrillo'
from cProfile import label
import os
import glob
from datetime import date
import numpy as np
from os import walk
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import matplotlib.ticker



def join_labels(string,extra=r""):
    str_day=string.split('/')[-2].split('-')[0:4]
    str_exp=string.split('/')[-1].split('.')[0]
    exp_label='-'.join(str_day)+' -'+str_exp+' '+extra
    return exp_label  


def rbackline(data,nopts,polgrade):
        datax=data[:,0]
        datay=data[:,1]
        backline=savgol_filter(datay,nopts,polgrade)
        datayrl = datay-backline
        dataout = np.array([datax,datayrl]).T
        class Results(): pass
        results          = Results()
        results.dataout  = dataout
        results.backline = backline
        return results

def rbdata(data):
    ldata = data.shape[0]
    for j in range(ldata):
        if data[j,1] > 1 or data[j,1] < -1:
            data[j,1] =  data[j-1,1]
    return data



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


class OOMFormatter(matplotlib.ticker.ScalarFormatter):
    def __init__(self, order=0, fformat="%1.1f", offset=True, mathText=True):
        self.oom = order
        self.fformat = fformat
        matplotlib.ticker.ScalarFormatter.__init__(self,useOffset=offset,useMathText=mathText)
    def _set_order_of_magnitude(self):
        self.orderOfMagnitude = self.oom
    def _set_format(self, vmin=None, vmax=None):
        self.format = self.fformat
        if self._useMathText:
            self.format = r'$\mathdefault{%s}$' % self.format




class adata(parameters):
    def __init__(self,inputfile,sample):
        if type(inputfile)==dict:
            inputfile=AttrDict(inputfile) 

        self.data=sample.data
        self.raspos1=sample.raspos1
        self.raspos2=sample.raspos2
        self.nameraspos1=sample.nameraspos1
        self.nameraspos2=sample.nameraspos2
        self.nameraspos=sample.nameraspos
        self.samplename=inputfile.samplename
        self.expi=inputfile.expi
        self.expf=inputfile.expf
        self.lendata=len(sample.data)
        self.filesname=sample.filesname
        self.truncdata=inputfile.truncdata # This variable defines where it starts the experiment's plots.
        self.rav=0
        self.rasav=0
        self.rasdata=[]
        self.rdata=[]
        self.nopts=inputfile.nopts
        self.polgrade=inputfile.polgrade


    def plotall(self):
        fig,ax = plt.subplots(nrows=1,ncols=2,figsize=(10,5))
        plt.subplots_adjust(wspace=0.2)
        ravx = 0
        ravy = 0
        count= 0
        self.rav = np.zeros((self.data[0][0].shape[0],2))
        for i in range(self.expi,self.expf):
            for j in range(self.truncdata,len(self.data[i])):
                self.datac=rbdata(self.data[i][j])
                lbl=join_labels(self.filesname[i][j]) if i>0 else join_labels(self.filesname[i][j])
                #ax[0].plot(self.data[i][j][:,0],self.data[i][j][:,1],lw=1,label=lbl)
                ax[0].plot(self.datac[:,0],self.datac[:,1],lw=1,label=lbl)
                r0=self.data[i][j][:,2]
                bgr=savgol_filter(r0,self.nopts,self.polgrade) 
                r1  = (r0-bgr)
                
                axins1 = inset_axes(ax[1], width="100%", height="100%",
                            bbox_to_anchor=(0.0,0.7,0.3,0.3),
                            bbox_transform=ax[1].transAxes,
                            borderpad=0,
                                )
                #
                axins1.set_xticks([])
                axins1.set_yticks([])
                axins1.plot(self.data[i][j][:,0],r0)
                axins1.plot(self.data[i][j][:,0],bgr,'r')
                ax[1].plot(self.data[i][j][:,0],r1,lw=1,alpha=1)
                count+=1

        ax[0].set_xlabel("Photon energy (eV)")    
        ax[1].set_xlabel("Photon energy (eV)")    
        ax[1].set_ylabel("R")    
        

        for axe in ax:
            axe.yaxis.set_major_formatter(OOMFormatter(-4, "%1.1f"))
            axe.ticklabel_format(axis='y', style='sci', scilimits=(-4,-4))

        ax[0].legend(frameon=False,fontsize=10)
        plt.show() 


    def plotras(self):
        fig,ax = plt.subplots(nrows=1,ncols=2,figsize=(10,5))
        plt.subplots_adjust(wspace=0.2)

        axins1 = inset_axes(ax[1], width="100%", height="100%",
                        bbox_to_anchor=(0.0,0.7,0.4,0.3),
                        bbox_transform=ax[1].transAxes,
                        borderpad=0,
                            )
        axins1.set_xticks([])
        axins1.set_yticks([])

        ravxp1 = 0
        ravyp1 = 0
        ravxp2 = 0
        ravyp2 = 0
        countp1= 0
        countp2= 0
        self.ravp1 = np.zeros((self.raspos1[0].shape[0],2))
        self.rasavp1 = np.zeros((self.raspos1[0].shape[0],2))
        self.ravp2 = np.zeros((self.raspos2[0].shape[0],2))
        self.rasavp2 = np.zeros((self.raspos2[0].shape[0],2))
        rasavxp1=0
        rasavyp1=0
        rasavxp2=0
        rasavyp2=0
        self.rasdatap1=[]
        self.rdatap1=[]
        self.rasdatap2=[]
        self.rdatap2=[]

        for i in range(self.truncdata,len(self.raspos1)):
            maxvals=np.max(self.raspos1[i][:,1])
            if maxvals>=1e-1 or maxvals<=-1e-1:
                pass
            else:
                lbl=join_labels(self.nameraspos1[i]) if i>0 else join_labels(self.nameraspos1[i])
                ax[0].plot(self.raspos1[i][:,0],self.raspos1[i][:,1],lw=1,label=lbl)

                r0=self.raspos1[i][:,2]
                bgr=savgol_filter(r0,self.nopts,self.polgrade) 
                r1  = (r0-bgr)
                #
                axins1.plot(self.raspos1[i][:,0],r0)
                axins1.plot(self.raspos1[i][:,0],bgr)
                ax[1].plot(self.raspos1[i][:,0],r1,lw=1,alpha=0.2)
                #averages
                ravyp1+=r1
                ravxp1+=self.raspos1[i][:,0]
                rasavxp1+=self.raspos1[i][:,0]
                rasavyp1+=self.raspos1[i][:,1]
                self.rasdatap1.append(np.array([self.raspos1[i][:,0],self.raspos1[i][:,1]]).T)
                self.rdatap1.append(np.array([self.raspos1[i][:,0],self.raspos1[i][:,2]]).T)
                countp1+=1

        for i in range(self.truncdata,len(self.raspos2)):
            maxvals=np.max(self.raspos2[i][:,1])
            if maxvals>=1e-1 or maxvals<=-1e-1:
                pass
            else:
                lbl=join_labels(self.nameraspos2[i]) if i>0 else join_labels(self.nameraspos2[i])
                ax[0].plot(self.raspos2[i][:,0],self.raspos2[i][:,1],lw=1,label=lbl)

                r0=self.raspos2[i][:,2]
                bgr=savgol_filter(r0,self.nopts,self.polgrade) 
                r1  = (r0-bgr)
                #
                axins1.plot(self.raspos2[i][:,0],r0)
                axins1.plot(self.raspos2[i][:,0],bgr)
                ax[1].plot(self.raspos2[i][:,0],r1,lw=1,alpha=0.2)
                #averages
                ravyp2+=r1
                ravxp2+=self.raspos2[i][:,0]
                rasavxp2+=self.raspos2[i][:,0]
                rasavyp2+=self.raspos2[i][:,1]
                self.rasdatap2.append(np.array([self.raspos2[i][:,0],self.raspos2[i][:,1]]).T)
                self.rdatap2.append(np.array([self.raspos2[i][:,0],self.raspos2[i][:,2]]).T)
                countp2+=1

        self.ravp1[:,0]=ravxp1/countp1
        self.ravp1[:,1]=ravyp1/countp1
        self.rasavp1[:,0]=rasavxp1/countp1
        self.rasavp1[:,1]=rasavyp1/countp1

        self.ravp2[:,0]=ravxp2/countp2
        self.ravp2[:,1]=ravyp2/countp2

        self.rasavp2[:,0]=rasavxp2/countp2
        self.rasavp2[:,1]=rasavyp2/countp2

        self.ravx = (self.ravp1[:,0]+self.ravp2[:,0])/2
        self.ravy = (self.ravp1[:,1]+self.ravp2[:,1])/2
        self.ravp = np.zeros((len(self.ravx),2))
        self.ravp[:,0]=self.ravx
        self.ravp[:,1]=self.ravy
        
        self.rasx = (self.rasavp1[:,0]+self.rasavp2[:,0])/2
        self.rasy = (self.rasavp1[:,1]-self.rasavp2[:,1])/2
        self.ras = np.zeros((len(self.rasx),2))
        self.ras[:,0]=self.rasx
        self.ras[:,1]=self.rasy

        ax[0].plot(self.ras[:,0],self.ras[:,1],lw=2,label="RAS")
        ax[0].plot(self.rasavp1[:,0],self.rasavp1[:,1],lw=2,label="RAS-Average-pos1")
        ax[0].plot(self.rasavp2[:,0],self.rasavp2[:,1],lw=2,label="RAS-Average-pos2")
        ax[1].plot(self.ravp[:,0],self.ravp[:,1],lw=2,label="Total Average R")
        
        ax[0].set_xlabel("Photon energy (eV)")    
        ax[0].set_ylabel("RAS")   
        ax[1].set_xlabel("Photon energy (eV)")    
        ax[1].set_ylabel("R")    
        

        for axe in ax:
            axe.yaxis.set_major_formatter(OOMFormatter(-4, "%1.1f"))
            axe.ticklabel_format(axis='y', style='sci', scilimits=(-4,-4))

        ax[0].legend(frameon=False,fontsize=7)
        ax[1].legend(frameon=False,fontsize=7)      

        plt.show() 

        class Results(): pass
        results          = Results()
        results.rasavp1=self.rasavp1
        results.rasavp2=self.rasavp2
        results.ras=self.ras
        results.ravp=self.ravp
        return results
        
    
    

        


# def CorrImag(datIm,grade,offset):
#     ImRes=np.zeros(datIm.shape)
#     for i in range(ImRes.shape[0]):
#         datnum=np.array(datIm[i,:])
    
#         x=np.arange(0,datnum.size)
#         a,b =np.polyfit(x,datnum,grade)
#         fit=a*x+b
#         ImRes[i,:]=fit-datnum+offset
#     return ImRes