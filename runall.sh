#!/bin/bash

maxproc=6

for data in "spe9/SPE9.DATA" "norne/NORNE_ATW2013.DATA"
do
    if [[ "$data" == "spe9/SPE9.DATA" ]]
    then
        casename="spe9"
    elif [[ "$data" == "norne/NORNE_ATW2013.DATA" ]]
    then
        casename="norne"
    fi
    for numproc in $(seq $maxproc)
    do
        for numthreads in 1 2
        do
            mpirun -np $numproc ~/opm/opm-simulators/build/bin/flow ~/opm/opm-data/$data --threads-per-process=$numthreads --output-dir=$casename"_processors"$numproc"_threads"$numthreads
        done
    done
done
