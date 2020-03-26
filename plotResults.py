#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 21:08:33 2020

@author: hnil
"""
#%%
from getData import *
import matplotlib.pyplot as pl
pl.rcParams.update({'font.size': 22})
#%%
#%ls data
#%%
maxproc=4
ran=np.arange(1,maxproc+1)
dataorigin="hnil-workstation_hnil_20:32:05-25-03-2020/"
cases=["NORNE_ATW2013"]
numthreadsvec = [1]
i=0
for casename in ["NORNE_ATW2013"]:
    i+=1
    pl.figure(i,figsize=(12,8))
    pl.clf() 
    pl.title('total time for case '+casename) 
    pl.xlabel('N = num processors') 
    pl.ylabel('t1/(N*tN) *100 %')

    for numthreads in numthreadsvec:
        if numthreads == 1:
                mark='o'
        else:
                mark='x'
        res=getTotalTime(dataorigin,casename,numthreads,maxproc)
        #res=getNewtonIterations(dataorigin,casename,numthreads,maxproc)
        #res=getLinearIterations(dataorigin,casename,numthreads,maxproc)
        #res=getLinearSolveTime(dataorigin,casename,numthreads,maxproc)
        #res=getAssemblyTime(dataorigin,casename,numthreads,maxproc)
        #res=getNumTotalCells(dataorigin,casename,numthreads,maxproc)
        #res=getNumOwnedCells(dataorigin,casename,numthreads,maxproc)
        #res=getNumOverlapCells(dataorigin,casename,numthreads,maxproc)
        pl.plot(ran,100*res[0]/(ran*res),'-'+mark,linewidth=4,markersize=12,label=dataorigin+" "+str(numthreads)+" threads")
    pl.legend()