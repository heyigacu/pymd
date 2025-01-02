#!/bin/bash

# Function: Display help information
show_help() {
    echo "Usage: $0 <cuda_device> <prmtop> <inpcrd> <num_residues> <temperature> <md_steps>"
    echo
    echo "Parameters:"
    echo "  cuda_device    CUDA device number (e.g., 0)"
    echo "  prmtop         Topology file path (e.g., com_solv.prmtop)"
    echo "  inpcrd         Initial coordinates file path (e.g., com_solv.inpcrd)"
    echo "  num_residues   Number of residues (e.g., 728)"
    echo "  temperature    Temperature in Kelvin (e.g., 310.0)"
    echo "  md_steps       Number of MD steps (e.g., 250000000)"
    echo
    echo "Example:"
    echo "nohup bash $0 0 com_solv.prmtop com_solv.inpcrd 285 310.0 250000000 &"
}

# Check if help is requested
if [[ "$1" == "-h" || "$1" == "--help" ]]; then
    show_help
    exit 0
fi

# Assign command-line arguments
cuda_device=$1
prmtop=$2
inpcrd=$3
num_residues=$4
temperature=$5
md_steps=$6

workdir=$(pwd)
echo $workdir

cat > $workdir/min.in << EOF
minimise
 &cntrl
  imin=1, maxcyc=2000, ncyc=100,
  ntc=1, ntf=1,
  ntp=0, ntb=1, cut=8.0,
  ntpr=100, ntwr=100,
  ntr=1, restraintmask=':1-$num_residues',
  restraint_wt=2.0
 /

EOF

cat > $workdir/nvt.in << EOF
heat NVT 200ps
&cntrl
  imin=0, irest=0, ntx=1,
  nstlim=100000, dt=0.002,
  ntc=2, ntf=2, 
  ntt=3, gamma_ln=2.0,
  ntp=0, ntb=1, cut=8.0,
  ntr=1, restraintmask=':1-$num_residues', restraint_wt=1.0,
  tempi=0.0, temp0=$temperature,
  iwrap=1,
  ig=-1,
  ntpr=1000, ntwx=1000, ntwr=10000,
/

&wt type='TEMP0', istep1=0, istep2=10000, value1=0.0, value2=$temperature, &end
&wt type='END', &end

EOF

cat > $workdir/npt.in << EOF
density NPT 200ps
&cntrl
  imin=0, irest=1, ntx=5,
  nstlim=100000, dt=0.002,
  ntc=2, ntf=2,
  ntt=3, gamma_ln=2.0,
  ntp=1, ntb=2, pres0=1.0, cut=8.0, taup=2.0,
  ntr=1, restraintmask=':1-$num_residues', restraint_wt=1.0,
  iwrap=1,
  ig=-1,
  tempi=$temperature, temp0=$temperature,
  ntpr=1000, ntwx=1000, ntwr=10000,
/

EOF

cat > $workdir/equil.in << EOF
equillibrium 500ps (no restraint)
&cntrl
  imin=0, irest=1, ntx=5,
  nstlim=250000,dt=0.002,
  ntc=2, ntf=2,
  ntt=3, gamma_ln=2.0,
  ntp=1, ntb=2, pres0=1.0, cut=8.0, taup=2.0,
  iwrap=1,
  ig=-1,
  tempi=$temperature, temp0=$temperature,
  ntpr=1000, ntwx=1000, ntwr=10000,
/

EOF

cat > $workdir/cmd.in << EOF
&cntrl
  imin=0, irest=0, ntx=1,
  ioutfm=1, nstlim=250000000,
  dt=0.002,
  tempi=$temperature, temp0=$temperature,
  ntc=2, ntf=1,
  ntt=3, gamma_ln=2.0,
  ntp=0, ntb=1, pres0=1.0, cut=8.0,
  iwrap = 1,
  ntr=0,
  ig=-1,
  ntpr=5000, ntwx=50000, ntwr=50000, ntwe=50000,
/

EOF


CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i min.in -o min.out -p $prmtop -c $inpcrd -r min.rst -ref $inpcrd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i nvt.in -o nvt.out -p $prmtop -c min.rst -r heat.rst -ref min.rst -x heat.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i npt.in -o npt.out -p $prmtop -c heat.rst -r density.rst -ref heat.rst -x density.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i equil.in -o equil.out -p $prmtop -c density.rst -r equil.rst -ref density.rst -x equil.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i cmd.in -o cmd.out -p $prmtop -c equil.rst -r cmd.rst -x cmd.dcd
