import sys
if sys.version_info < (3, 5):
    raise "must use python 3.5 or greater"
import os

import subprocess
import numpy as np

def parse(command):
    return subprocess.run([command, '-l'], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8')

def get_totalTime(casename, numthreads, maxproc):
    res=np.zeros(maxproc)
    for numprocessors in np.arange(1,maxproc+1):
        dn="sims/"+casename+"_processors"+str(numprocessors)+"_threads"+str(numthreads)
        command='tail -n30 '+dn+'/*DBG|grep "Total time (seconds)"|cut -d ":" -f 2'
        res[numprocessors-1] = float(parse(command))
    return res

def get_numNewtonIterations(casename, numthreads, maxproc):
    res=np.zeros(maxproc)
    for numprocessors in np.arange(1,maxproc+1):
        dn="sims/"+casename+"_processors"+str(numprocessors)+"_threads"+str(numthreads)
        command='tail -n30 '+dn+'/*DBG|grep "Newton Iterations"|cut -d ":" -f 2|cut -d " " -f 5'
        res[numprocessors-1] = int(parse(command))
    return res

def get_numLinearIterations(casename, numthreads, maxproc):
    res=np.zeros(maxproc)
    for numprocessors in np.arange(1,maxproc+1):
        dn="sims/"+casename+"_processors"+str(numprocessors)+"_threads"+str(numthreads)
        command='tail -n30 '+dn+'/*DBG|grep "Linear Iterations"|cut -d ":" -f 2|cut -d " " -f 5'
        res[numprocessors-1] = int(parse(command))
    return res

def get_AssemplyTime(casename, numthreads, maxproc):
    res=np.zeros(maxproc)
    for numprocessors in np.arange(1,maxproc+1):
        dn="sims/"+casename+"_processors"+str(numprocessors)+"_threads"+str(numthreads)
        command='tail -n30 '+dn+'/*DBG|grep "Assembly time (seconds)"|cut -d ":" -f 2|cut -d " " -f 6'
        res[numprocessors-1] = float(parse(command))
    return res

def get_linearSolveTime(casename, numthreads, maxproc):
    res=np.zeros(maxproc)
    for numprocessors in np.arange(1,maxproc+1):
        dn="sims/"+casename+"_processors"+str(numprocessors)+"_threads"+str(numthreads)
        command='tail -n30 '+dn+'/*DBG|grep "Linear solve time (seconds)"|cut -d ":" -f 2|cut -d " " -f 2'
        res[numprocessors-1] = float(parse(command))
    return res

def get_numCells(casename, numthreads, maxproc):
    res=np.zeros((maxproc,maxproc))
    for numprocessors in np.arange(2,maxproc+1):
        dn="sims/"+casename+"_processors"+str(numprocessors)+"_threads"+str(numthreads)
        if numprocessors == 2:
            command = 'grep -i load '+dn+'/*DBG|cut -d " " -f 4'
            totalactivecells = int(parse(command))
            res[0,0] = totalactivecells
        command='line=`grep -i load '+dn+'/*DBG -n`; linenumber=`echo $line|cut -d ":" -f 1`; numprocs=`echo $line|cut -d " " -f 8`; linenumber=`expr $linenumber + 3`; data=`tail -n+$linenumber '+dn+'/*DBG | head -n$numprocs`; count=0;for d in $data; do if [ `expr $count % 2` -eq 1 ]; then echo $d", "; fi; count=`expr $count + 1`; done'
        data = str(parse(command))
        for i in np.arange(0,numprocessors):
            res[numprocessors-1,i] = int(data.split(', ')[i])
    return res

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
    res=get_numCells(casename, numthreads, maxproc)
    np.save(name+"_numCells",res)


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
