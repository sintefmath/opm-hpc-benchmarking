#!/bin/bash

echo "import numpy as np" > plottotaltimes.py
echo "import pylab as pl" >> plottotaltimes.py
for data in "spe9/SPE9.DATA" "norne/NORNE_ATW2013.DATA"
do
    if [[ "$data" == "spe9/SPE9.DATA" ]]
    then
        casename="spe9"
    elif [[ "$data" == "norne/NORNE_ATW2013.DATA" ]]
    then
        casename="norne"
    fi
    echo "pl.figure()" >> plottotaltimes.py
    echo "pl.title('"strong scaling for case $casename"')" >> plottotaltimes.py
    echo "pl.xlabel('N = num processors')" >> plottotaltimes.py
    echo "pl.ylabel('t1/(N*tN) *100 %')" >> plottotaltimes.py
    echo "ran=np.arange(1,7)" >> plottotaltimes.py
    for numthreads in 1 2
    do
	str=$casename"_"$numthreads"=np.array(["
        for numprocessors in 1 2 3 4 5 6
        do
            dn=$casename"_processors"$numprocessors"_threads"$numthreads
	    totaltime=`tail -n30 $dn/*DBG|grep "Total time (seconds)"|cut -d ":" -f 2`
	    str+=$totaltime", "
        done
	str+="])"
	echo $str >> plottotaltimes.py
	echo "t1="$casename"_"$numthreads"[0]" >> plottotaltimes.py
	echo "pl.plot(ran,100*t1/(ran*"$casename"_"$numthreads"),'x-',label='"$numthreads" threads')" >> plottotaltimes.py
    done
    echo "pl.legend()" >> plottotaltimes.py
    echo "pl.savefig('total_times_"$casename"')" >> plottotaltimes.py
    python plottotaltimes.py
done
