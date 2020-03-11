import sys
if sys.version_info < (3, 5):
    raise "must use python 3.5 or greater"
import os
import os.path
from os import path

import subprocess
import numpy as np

def parse(command):
    return subprocess.run([command, '-l'], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')

def getdebugfile(casename, numthreads, numprocessors):
    return "sims/"+casename+"_processors"+str(numprocessors)+"_threads"+str(numthreads)+'/'+casename+'.DBG'

def get_totalTime(casename, numthreads, maxproc):
    res=np.empty(maxproc)
    res[:] = np.nan
    for numprocessors in np.arange(1,maxproc+1):
        dbgf=getdebugfile(casename,numthreads, numprocessors)
        if path.exists(dbgf):
            command='tail -n30 '+dbgf+'|grep "Total time (seconds)"|cut -d ":" -f 2'
            tmp=parse(command).strip()
            if tmp:
                res[numprocessors-1] = float(tmp)
    return res

def get_numNewtonIterations(casename, numthreads, maxproc):
    res=np.empty(maxproc)
    res[:] = np.nan
    for numprocessors in np.arange(1,maxproc+1):
        dbgf=getdebugfile(casename,numthreads, numprocessors)
        if path.exists(dbgf):
            command='tail -n30 '+dbgf+'|grep "Newton Iterations"|cut -d ":" -f 2|cut -d " " -f 5'
            tmp=parse(command).strip()
            if tmp:
                res[numprocessors-1] = int(tmp)
    return res

def get_numLinearIterations(casename, numthreads, maxproc):
    res=np.empty(maxproc)
    res[:] = np.nan
    for numprocessors in np.arange(1,maxproc+1):
        dbgf=getdebugfile(casename,numthreads, numprocessors)
        if path.exists(dbgf):
            command='tail -n30 '+dbgf+'|grep "Linear Iterations"|cut -d ":" -f 2|cut -d " " -f 5'
            tmp=parse(command).strip()
            if tmp:
                res[numprocessors-1] = int(tmp)
    return res

def get_AssemplyTime(casename, numthreads, maxproc):
    res=np.empty(maxproc)
    res[:] = np.nan
    for numprocessors in np.arange(1,maxproc+1):
        dbgf=getdebugfile(casename,numthreads, numprocessors)
        if path.exists(dbgf):
            command='tail -n30 '+dbgf+'|grep "Assembly time (seconds)"|cut -d ":" -f 2|cut -d " " -f 6'
            tmp=parse(command).strip()
            if tmp:
                res[numprocessors-1] = float(tmp)
    return res

def get_linearSolveTime(casename, numthreads, maxproc):
    res=np.empty(maxproc)
    res[:] = np.nan
    for numprocessors in np.arange(1,maxproc+1):
        dbgf=getdebugfile(casename,numthreads, numprocessors)
        if path.exists(dbgf):
            command='tail -n30 '+dbgf+'|grep "Linear solve time (seconds)"|cut -d ":" -f 2|cut -d " " -f 2'
            tmp=parse(command).strip()
            if tmp:
                res[numprocessors-1] = float(tmp)
    return res

def get_numCells(casename, numthreads, maxproc):
    owned=np.empty((maxproc,maxproc))
    owned[:] = np.nan
    overlap=np.empty((maxproc,maxproc))
    overlap[:] = np.nan
    total=np.empty((maxproc,maxproc))
    total[:] = np.nan
    for numprocessors in np.arange(2,maxproc+1):
        dbgf=getdebugfile(casename,numthreads, numprocessors)
        if path.exists(dbgf):
            if numprocessors == 2:
                command = 'grep -i load '+dbgf+'|cut -d " " -f 4'
                tmp = parse(command)
                if tmp:
                    total[0,0] = int(tmp)
            command='line=`grep -i load '+dbgf+' -n`; linenumber=`echo $line|cut -d ":" -f 1`; linenumber=`expr $linenumber + 3`; echo $linenumber'
            linenumber = str(parse(command)).strip()
            if int(linenumber)>3:### if the line is not found, linenumber will be 3
                #owned
                rest=str(1)
                command='data=`tail -n+'+linenumber+' '+dbgf+' | head -n'+str(numprocessors)+'`; count=0;for d in $data; do if [ `expr $count % 4` -eq '+rest+' ]; then echo $d", "; fi; count=`expr $count + 1`; done'
                data = str(parse(command))
                for i in np.arange(0,numprocessors):
                    owned[numprocessors-1,i] = float(data.split(', ')[i])
                #overlap
                rest=str(2)
                command='data=`tail -n+'+linenumber+' '+dbgf+' | head -n'+str(numprocessors)+'`; count=0;for d in $data; do if [ `expr $count % 4` -eq '+rest+' ]; then echo $d", "; fi; count=`expr $count + 1`; done'
                data = str(parse(command))
                for i in np.arange(0,numprocessors):
                    overlap[numprocessors-1,i] = float(data.split(', ')[i])
                #total
                rest=str(3)
                command='data=`tail -n+'+linenumber+' '+dbgf+' | head -n'+str(numprocessors)+'`; count=0;for d in $data; do if [ `expr $count % 4` -eq '+rest+' ]; then echo $d", "; fi; count=`expr $count + 1`; done'
                data = str(parse(command))
                for i in np.arange(0,numprocessors):
                    total[numprocessors-1,i] = float(data.split(', ')[i])
    return owned, overlap, total

def writedata(foldername, casename, numthreads, maxproc):
    name=foldername+"/"+casename
    name+="_threads_"+str(numthreads)
    res=get_totalTime(casename, numthreads, maxproc)
    np.save(name+"_totaltime",res)
    res=get_numNewtonIterations(casename, numthreads, maxproc)
    np.save(name+"_newtoniterations",res)
    res=get_numLinearIterations(casename, numthreads, maxproc)
    np.save(name+"_lineariterations",res)
    res=get_AssemplyTime(casename, numthreads, maxproc)
    np.save(name+"_assemblytime",res)
    res=get_linearSolveTime(casename, numthreads, maxproc)
    np.save(name+"_linearsolvetime",res)
    owned, overlap, total=get_numCells(casename, numthreads, maxproc)
    np.save(name+"_numOwnedCells",owned)
    np.save(name+"_numOverlapCells",overlap)
    np.save(name+"_numTotalCells",total)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Parse and write data')
    parser.add_argument('--maxproc', metavar='maxproc', required=True,
                        type=int, help='maximum number of processors')
    parser.add_argument('--maxthreads', metavar='maxthreads', required=True,
                        type=int, help='maximum number of threads')
    args = parser.parse_args()

    foldername="data/"+str(parse("uname --nodename")).strip()
    foldername+="_"+str(parse("whoami")).strip()
    foldername+="_"+str(parse('date +"%T-%d-%m-%Y"')).strip()
    
    if not os.path.exists(foldername):
        os.makedirs(foldername)

    for numthreads in np.arange(1,args.maxthreads+1):
        writedata(foldername, "NORNE_ATW2013",numthreads, args.maxproc)
        writedata(foldername, "SPE9",numthreads, args.maxproc)
