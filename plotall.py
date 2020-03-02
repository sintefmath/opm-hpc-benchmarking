import sys
if sys.version_info < (3, 5):
    raise "must use python 3.5 or greater"

import numpy as np
import matplotlib.pyplot as pl

def getName(foldername, casename, numthreads, maxproc):
    name="data/"+foldername
    name+=casename+"_threads_"+str(numthreads)
    return name

def getTotalTime(foldername, casename, numthreads, maxproc):
    name=getName(foldername, casename, numthreads, maxproc)
    res = np.load(name+"_totaltime.npy")
    return res

def getNewtonIterations(foldername, casename, numthreads, maxproc):
    name=getName(foldername, casename, numthreads, maxproc)
    res=np.load(name+"_newtoniterations.npy")
    return res

def getLinearIterations(foldername, casename, numthreads, maxproc):
    name=getName(foldername, casename, numthreads, maxproc)
    res=np.load(name+"_lineariterations.npy")
    return res

def getAssemblyTime(foldername, casename, numthreads, maxproc):
    name=getName(foldername, casename, numthreads, maxproc)
    res=np.load(name+"_assemblytime.npy")
    return res

def getLinearSolveTime(foldername, casename, numthreads, maxproc):
    name=getName(foldername, casename, numthreads, maxproc)
    res=np.load(name+"_linearsolvetime.npy")
    return res

def getNumCells(foldername, casename, numthreads, maxproc):
    name=getName(foldername, casename, numthreads, maxproc)
    res=np.load(name+"_numCells.npy")
    return res
