#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 21:08:33 2020

@author: hnil
"""
#%%
#from getData import *
import getDataField as gd
import matplotlib.pyplot as pl
pl.rcParams.update({'font.size': 14})
#%%
#%ls data
#%%
class PlotType:
    def __init__(self,name,func):
        self.name = name
        self.func = func
#%%        
maxproc=20
ran=np.arange(1,maxproc+1)
dataorigin="hnil-workstation_hnil_20:32:05-25-03-2020/"
dataorigin="hnil-workstation_hnil_09:19:43-26-03-2020/"
#dataorigin="hnil-workstation_hnil_20:03:31-26-03-2020/"
cases=["NORNE_ATW2013","SPE9"]
numthreadsvec = [1,2]
fields = gd.getFields()
timefields = fields[0:3]
i=0
plottype={}

#%%
a= (lambda x,y: x/y)
plottypes =[PlotType("relative eff",(lambda ref,res,ran: ref/(ran*res))),
            PlotType("relative speedup",(lambda ref,res,ran: ref/res))] 
#%%
#fig,clf
#plottypes = [plottypes[0]]
close("all")
for plottype in plottypes:
    fig, axs = plt.subplots(1, 3, figsize=(12, 8), sharey=True,sharex=True)
    
    for casename in ["NORNE_ATW2013","SPE9"]:
        i=0
        for field in timefields:
            res_ref = gd.getField(dataorigin,casename,1,1,field);
            res_ref = res_ref[0];
            #pl.figure(i,figsize=(12,8))
            #pl.clf() 
            aix=i
            #aiy=i%2
            ax=axs[aix]
            #ax.title('%s for case %s ' %(field,casename)) 
            #ax.xlabel('N = num processors') 
            #ax.ylabel('t1/(N*tN) *100 %')
    
            
            for numthreads in numthreadsvec:
                if numthreads == 1:
                    mark='o'
                else:
                    mark='x'
                res = gd.getField(dataorigin,casename,numthreads,maxproc,field)
                assert(len(res) == len(ran))
                #sfig = ax.plot(ran,100*res[0]/(ran*res),'-'+mark,linewidth=4,markersize=12,label=dataorigin+" "+str(numthreads)+" threads")
                #sfig = ax.plot(ran,plottype.func(res_ref,res,ran),'-'+mark,linewidth=4,markersize=12,label=dataorigin+" "+str(numthreads)+" threads")
                sfig = ax.plot(ran,plottype.func(res_ref,res,ran),'-'+mark,linewidth=4,markersize=12,label=casename +" "+str(numthreads)+" threads")
            #pl.legend()
            ax.set_title('%s ' %(field))
            ax.set_ylabel('t1/(N*tN) *100 %')
            ax.set_xlabel('N = num processors') 
            pl.legend()
            i=i+1
            print(i)
    fig.suptitle(casename + " " + plottype.name)

#%%
 plottypes =[PlotType("relative",(lambda ref,res: 100*res/ref)),
            PlotType("absolut",(lambda ref,res: res))]    
#close("all") 
fields = gd.getFields()
numfields =fields[-3:]
for field in numfields:
    i=0
    for casename in cases:
        fig, axs = plt.subplots(1, 2, figsize=(12, 8), sharey=False,sharex=True)
        #pl.figure(i,figsize=(12,8))
        #pl.clf() 
        #pl.title('Cell overlap distribution '+casename) 
        #pl.xlabel('N = num processors') 
        #pl.ylabel('overlap')
        i=0
        for plottype in plottypes:
            ax = axs[i]
            numthreads=numthreadsvec[0]
            res=gd.getField(dataorigin,casename,numthreads,maxproc,field)
            if field == "numOverlapCells":
               resv=gd.getField(dataorigin,casename,numthreads,maxproc,"numTotalCells")
               ref=resv[0][0]
            else:
                ref=res[0][0]
                
            for j in np.arange(2,maxproc+1):
                for k in np.arange(0,j):
                    if numthreads == 1:
                        mark='o'
                    else:
                        mark='x'
                    pres = res[j-1,k]   
                    ax.plot(j-1,plottype.func(ref,pres),'og',linewidth=4,markersize=12)
            ax.set_title('%s ' %(field))
            if plottype.name == "relative":
                ax.set_ylabel('t1/(N*tN) *100 %')
            else:
                ax.set_ylabel('N')
            ax.set_xlabel('N = num processors')    
            i=i+1
        fig.suptitle(casename)
#%%
 i=0
numthreads=numthreadsvec[0]
for casename in cases:
    i+=1
    pl.figure(i,figsize=(8,8))
    pl.clf() 
    pl.title('Speedup comparison '+casename) 
    pl.xlabel('N = num processors') 
    pl.ylabel('speedup')

    numthreads=1
    overlapcell=gd.getField(dataorigin,casename,numthreads,maxproc,'numOverlapCells')
    ownedcell=gd.getField(dataorigin,casename,numthreads,maxproc,'numOwnedCells')
    totalcell=gd.getField(dataorigin,casename,numthreads,maxproc,'numTotalCells')
    tmp=np.ones(maxproc)
    for j in np.arange(1,maxproc):
        largestpartition = np.nanmax(totalcell[j,:])
        tmp[j] = totalcell[0,0]/largestpartition
    #pl.plot(j, tmp,'ok',linewidth=4,markersize=12,label="maximum first order partition speedup")
    pl.plot(ran, tmp,'ok-',linewidth=4,markersize=12,label="maximum first order partition speedup")
    pl.plot(ran, ran,'--',linewidth=4,markersize=12,label="optimal")
    pl.legend()
    pl.axis([0,maxproc,0,maxproc])
i=0
numthreads=2
for casename in cases:
    i+=1
    pl.figure(i,figsize=(12,8))
    #pl.clf() 
    pl.title('Speedup comparison '+casename) 
    pl.xlabel('N = num processors') 
    pl.ylabel('speedup')
    for field in timefields:
        res = gd.getField(dataorigin,casename,numthreads,maxproc,field)             
        pl.plot(ran,res[0]/(res),'-'+mark,linewidth=4,markersize=12,label="actual speedup " + field)
    pl.legend()