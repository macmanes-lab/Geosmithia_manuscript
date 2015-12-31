#!/bin/sh

# Ready MPI library
export LD_PRELOAD="/usr/lib/libmpi.so:$LD_PRELOAD"

mpirun -np $1 /opt/maker/bin/maker -fix_nucleotide -base $2
                