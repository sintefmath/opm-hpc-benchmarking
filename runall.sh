#!/bin/bash

###########################
# 1) parse arguments
###########################

issaga=False
if [[ "`uname --nodename|cut -d "." -f2,3`" == "saga.sigma2" ]]; then
    issaga=True
fi

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

if [[ ! -d sims ]]; then
    mkdir sims
fi
cd sims/

for data in $cases
do
    casename="$(basename -s .DATA $data)"
    casefullfoldername="$(dirname $data)"
    casefoldername="$(basename $(dirname $data))"
    for numproc in $(seq $maxproc)
    do
        for numthreads in $(seq $maxthreads)
        do
            name=$casename"_processors"$numproc"_threads"$numthreads
            fname=$name".sh"

            if [[ ! $issaga == "True" ]]; then
                mpirun -np $numproc $flowdir/flow $data --threads-per-process=$numthreads --output-dir=$casename"_processors"$numproc"_threads"$numthreads
            else
                if [[ ! -d $name ]]; then
                    mkdir -p $name
                fi

                (
                    cd $name
                    echo "#!/bin/bash" > $fname
                    echo "#SBATCH --account=NN9766K" >> $fname
                    echo "#SBATCH --job-name="$name >> $fname
                    echo "#SBATCH --time=0-01:00:00" >> $fname
                    echo "#SBATCH --mem-per-cpu=3G" >> $fname
                    echo "#SBATCH --ntasks="$numproc" --cpus-per-task="$numthreads >> $fname

                    echo "set -o errexit # Make bash exit on any error" >> $fname
                    echo "set -o nounset # Treat unset variables as errors" >> $fname
                    echo "module --quiet purge" >> $fname
                    echo "module load Boost/1.71.0-GCC-8.3.0" >> $fname
                    echo "module load OpenMPI/3.1.4-GCC-8.3.0" >> $fname
                    echo "module load OpenBLAS/0.3.7-GCC-8.3.0" >> $fname
                    echo "module list" >> $fname

                    ###echo "workdir=\$USERWORK/$name" >> $fname
                    ###echo "mkdir -p \$workdir" >> $fname
                    ###echo "cp -r "$casefullfoldername" \$workdir" >> $fname
                    ###echo "cd \$workdir" >> $fname

                    echo "cp -r "$casefullfoldername" \$SCRATCH" >> $fname
                    echo "cd \$SCRATCH" >> $fname

                    echo "savefile output/*DBG " >> $fname

                    echo "time mpirun "$flowdir"flow $casefoldername/$casename.DATA --threads-per-process=$numthreads --output-dir=output" >> $fname
                    echo "exit 0" >> $fname

                    sbatch $fname
                )
            fi 
            
        done
    done
done
