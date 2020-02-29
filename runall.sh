#!/bin/bash

###########################
# 1) parse arguments
###########################

maxproc=""
flowdir=""
cases=""
maxthreads=""

count=0
args=(${@})
argsleft=$#

if [ $# == 0 ]; then
    echo "please specify the maximum number of precessors with --maxproc";
    exit 1
else
    while [[ $argsleft -gt 0 ]]; do
        arg=${args[count]}
        (( count++ ))
        (( argsleft-- ))

        case $arg in
        --maxproc)
            if [[ $argsleft -gt 0 ]]; then
                if   [ ${args[count]} == "--maxthreads" ] \
                    || [ ${args[count]} == "--flowdir" ] \
                    || [ ${args[count]} == "--data" ] \
                ; then
                    break;
                else
                    maxproc=${args[count]}
                    (( count++ ))
                    (( argsleft-- ))
                fi
            fi
            ;;
        --maxthreads)
            if [[ $argsleft -gt 0 ]]; then
                if   [ ${args[count]} == "--maxproc" ] \
                    || [ ${args[count]} == "--flowdir" ] \
                    || [ ${args[count]} == "--data" ] \
                ; then
                    break;
                else
                    maxthreads=${args[count]}
                    (( count++ ))
                    (( argsleft-- ))
                fi
            fi
            ;;
        --flowdir)
            if [[ $argsleft -gt 0 ]]; then
                if   [ ${args[count]} == "--maxproc" ] \
                    || [ ${args[count]} == "--maxthreads" ] \
                    || [ ${args[count]} == "--data" ] \
                ; then
                    break;
                else
                    flowdir=${args[count]}
                    (( count++ ))
                    (( argsleft-- ))
                fi
            fi
            ;;
        --data)
            while [[ $argsleft -gt 0 ]]; do
                if   [ ${args[count]} == "--maxproc" ] \
                    || [ ${args[count]} == "--maxthreads" ] \
                    || [ ${args[count]} == "--flowdir" ] \
                ; then
                    break;
                else
                    cases+=" "${args[count]}
                    (( count++ ))
                    (( argsleft-- ))
                fi
            done
            ;;
        *)
            echo "unknown option:" $arg;
            ;;
        esac
        shift # past argument or value
    done
fi

if [[ $maxproc == "" ]]; then
    echo "please specify the maximum number of precessors with --maxproc";
    exit 1
fi

if [[ $maxthreads == "" ]]; then
    echo "please specify the maximum number of threads with --maxthreads";
    exit 1
fi

if [[ $flowdir == "" ]]; then
    echo "please specify the flow directory with --flowdir"
    exit 1
fi

if [[ $cases == "" ]]; then
    echo "please specify the cases you want to run with --data, e.g., --data dir1/spe9/SPE9.DATA dir2/norne/NORNE_ATW2013.DATA"
    exit 1
fi

re='^[0-9]+$'
if ! [[ $maxproc =~ $re ]] ; then
    echo "maxproc is not a number" >&2
    exit 1
fi

if ! [[ $maxthreads =~ $re ]] ; then
    echo "maxthreads is not a number" >&2
    exit 1
fi

if [[ ! -d $flowdir ]]; then
    echo "flowdir is not a directory" >&2
    exit 1
fi

for data in $cases
do
    casename="$(basename -s .DATA $data)"
    for numproc in $(seq $maxproc)
    do
        for numthreads in $(seq $maxthreads)
        do
            mpirun -np $numproc $flowdir/flow ~/opm/opm-data/$data --threads-per-process=$numthreads --output-dir=$casename"_processors"$numproc"_threads"$numthreads
        done
    done
done
