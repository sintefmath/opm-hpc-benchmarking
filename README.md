# opm-hpc-benchmarking
scripts to perform benchmarking of opm on hpc

example usage:

1. ./runall.sh --maxproc 12 --flowdir ~/opm/opm-simulators/build/bin/ --data ~/opm/opm-data/norne/NORNE_ATW2013.DATA ~/opm/opm-data/spe9/SPE9.DATA --maxthreads 2
2. python parseall.py --maxthreads=2 --maxproc=12 
3. plot, e.g., use jupyter notebook
