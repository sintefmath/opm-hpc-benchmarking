import sys
if sys.version_info < (3, 5):
    raise "must use python 3.5 or greater"

import subprocess
maxproc=6

import numpy as np
import pylab as pl

def plotdata(casename, maxproc=6):
    """
    maxproc: maximum number of processors
    """

    pl.figure(1)
    pl.clf()
    pl.title('total time for case '+casename)
    pl.xlabel('N = num processors')
    pl.ylabel('t1/(N*tN) *100 %')

    pl.figure(2)
    pl.clf()
    pl.title('speedup of total time for case '+casename)
    pl.xlabel('N = num processors')
    pl.ylabel('t1/tN *100 %')

    pl.figure(3)
    pl.clf()
    pl.title('Newton iterations for case '+casename)
    pl.xlabel('N = num processors')
    pl.ylabel('# Newton iterations')

    pl.figure(4)
    pl.clf()
    pl.title('linear iterations for case '+casename)
    pl.xlabel('N = num processors')
    pl.ylabel('# Linear iterations')

    pl.figure(5)
    pl.clf()
    pl.title('linear solve time for case '+casename)
    pl.xlabel('N = num processors')
    pl.ylabel('t1/(N*tN) *100 %')

    pl.figure(6)
    pl.clf()
    pl.title('speedup of linear solve time for case '+casename)
    pl.xlabel('N = num processors')
    pl.ylabel('t1/tN *100 %')

    pl.figure(7)
    pl.clf()
    pl.title('assembly time for case '+casename)
    pl.xlabel('N = num processors')
    pl.ylabel('t1/(N*tN) *100 %')

    pl.figure(8)
    pl.clf()
    pl.title('speedup of assembly time for case '+casename)
    pl.xlabel('N = num processors')
    pl.ylabel('t1/tN *100 %')

    ran=np.arange(1,maxproc+1)
    for numthreads in [1, 2]:
        totaltime=np.zeros(maxproc)
        newtoniterations=np.zeros(maxproc)
        lineariterations=np.zeros(maxproc)
        assemblytime=np.zeros(maxproc)
        linearsolvetime=np.zeros(maxproc)
        if numthreads == 1:
                mark='o'
        else:
                mark='x'

        for numprocessors in ran:
            dn=casename+"_processors"+str(numprocessors)+"_threads"+str(numthreads)

            command='tail -n30 '+dn+'/*DBG|grep "Total time (seconds)"|cut -d ":" -f 2'
            totaltime[numprocessors-1] = float(subprocess.run([command, '-l'], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))

            command='tail -n30 '+dn+'/*DBG|grep "Newton Iterations"|cut -d ":" -f 2|cut -d " " -f 5'
            newtoniterations[numprocessors-1] = float(subprocess.run([command, '-l'], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))

            command='tail -n30 '+dn+'/*DBG|grep "Linear Iterations"|cut -d ":" -f 2|cut -d " " -f 5'
            lineariterations[numprocessors-1] = float(subprocess.run([command, '-l'], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))

            command='tail -n30 '+dn+'/*DBG|grep "Assembly time (seconds)"|cut -d ":" -f 2|cut -d " " -f 6'
            assemblytime[numprocessors-1] = float(subprocess.run([command, '-l'], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))

            command='tail -n30 '+dn+'/*DBG|grep "Linear solve time (seconds)"|cut -d ":" -f 2|cut -d " " -f 2'
            linearsolvetime[numprocessors-1] = float(subprocess.run([command, '-l'], stdout=subprocess.PIPE, shell=True).stdout.decode('utf-8'))

        pl.figure(1)
        pl.plot(ran,100*totaltime[0]/(ran*totaltime),'-'+mark,label=str(numthreads)+" threads")

        pl.figure(2)
        pl.plot(ran,100*totaltime[0]/totaltime,'-'+mark,label=str(numthreads)+" threads")

        pl.figure(3)
        pl.plot(ran,newtoniterations,'-'+mark,label=str(numthreads)+" threads")

        pl.figure(4)
        pl.plot(ran,lineariterations,'-'+mark,label=str(numthreads)+" threads")

        pl.figure(5)
        pl.plot(ran,100*assemblytime[0]/(ran*assemblytime),'-'+mark,label=str(numthreads)+" threads")

        pl.figure(6)
        pl.plot(ran,100*assemblytime[0]/assemblytime,'-'+mark,label=str(numthreads)+" threads")

        pl.figure(7)
        pl.plot(ran,100*linearsolvetime[0]/(ran*linearsolvetime),'-'+mark,label=str(numthreads)+" threads")

        pl.figure(8)
        pl.plot(ran,100*linearsolvetime[0]/linearsolvetime,'-'+mark,label=str(numthreads)+" threads")

    pl.figure(1)
    pl.legend()
    pl.savefig('total_times_'+casename)

    pl.figure(2)
    pl.legend()
    pl.savefig('speedup_total_times_'+casename)

    pl.figure(3)
    pl.legend()
    pl.savefig('newtoniterations_'+casename)

    pl.figure(4)
    pl.legend()
    pl.savefig('lineariterations_'+casename)

    pl.figure(5)
    pl.legend()
    pl.savefig('assemblytime_'+casename)

    pl.figure(6)
    pl.legend()
    pl.savefig('speedup_assemblytime_'+casename)

    pl.figure(7)
    pl.legend()
    pl.savefig('linearsolvetime_'+casename)

    pl.figure(8)
    pl.legend()
    pl.savefig('speedup_linearsolvetime_'+casename)



if __name__ == "__main__":
    plotdata("spe9")
    plotdata("norne")
