import sys
if sys.version_info < (3, 5):
    raise "must use python 3.5 or greater"

import numpy as np
import matplotlib.pyplot as pl

def getName(foldername, casename, numthreads, maxproc):
    name="data/"+foldername
    name+=casename+"_threads_"+str(numthreads)
    return name

def getField(foldername, casename, numthreads, maxproc,field):
    name=getName(foldername, casename, numthreads, maxproc)
    print(name)
    res = np.load(name+"_" + field + ".npy")
    return res

def getFields():
    res=["assemblytime",
         "linearsolvetime",
         "totaltime",
         "newtoniterations",
         "lineariterations",
         "numOwnedCells",
         "numOverlapCells",
         "numTotalCells"]     
    return res
