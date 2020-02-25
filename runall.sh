#!/bin/bash

for data in "spe9/SPE9.DATA" "norne/NORNE_ATW2013.DATA"
do
    if [[ "$data" == "spe9/SPE9.DATA" ]]
    then
        casename="spe9"
    elif [[ "$data" == "norne/NORNE_ATW2013.DATA" ]]
    then
        casename="norne"
    fi
    for numprocessors in 1 2 3 4 5 6
    do
        for numthreads in 1 2
        do
            mpirun -np $numprocessors ~/opm/opm-simulators/build/bin/flow ~/opm/opm-data/$data --threads-per-process=$numthreads --output-dir=$casename"_processors"$numprocessors"_threads"$numthreads
        done
    done
done
