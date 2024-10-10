#!bin/bash
workdir=$(pwd)
cuda_device=1
num_residues=728
no_ligand=728
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
  tempi=0.0, temp0=300.0,
  iwrap=1,
  ig=-1,
  ntpr=1000, ntwx=1000, ntwr=10000,
/

&wt type='TEMP0', istep1=0, istep2=10000, value1=0.0, value2=300.0, &end
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
  tempi=310.0, temp0=310.0,
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
  tempi=310.0, temp0=310.0,
  ntpr=1000, ntwx=1000, ntwr=10000,
/

EOF

cat > $workdir/md_pre.in << EOF
&cntrl
  imin=0, irest=0, ntx=1,
  ioutfm=1, nstlim=30000000,
  dt=0.002,
  tempi=310.0, temp0=310.0,
  ntc=2, ntf=1,
  ntt=3, gamma_ln=5.0,
  ntp=0, ntb=1, pres0=1.0, cut=8.0,
  iwrap = 1,
  ntr=0,
  ig=-1,
  ntpr=5000, ntwx=50000, ntwr=50000, ntwe=50000,

  igamd=3, irest_gamd=0,
  ntcmd=3000000, nteb=27000000, ntave=300000,
  ntcmdprep=900000, ntebprep=600000,
  sigma0P=6.0, sigma0D=6.0, iE=1,
/

EOF

cat > $workdir/prod.in << EOF
&cntrl
  imin=0, irest=1, ntx=5,
  ioutfm=1, nstlim=500000000,
  dt=0.002,
  tempi=310.0, temp0=310.0,
  ntc=2, ntf=1,
  ntt=3, gamma_ln=5.0,
  ntp=0, ntb=1, pres0=1.0, cut=8.0,
  iwrap = 1,
  ntr=0,
  ig=-1,
  ntpr=5000, ntwx=50000, ntwr=50000, ntwe=50000,

  igamd=3, irest_gamd=1,
  ntcmd=0, nteb=0, ntave=300000,
  ntcmdprep=0, ntebprep=0,
  sigma0P=6.0, sigma0D=6.0, iE=1,
/

EOF

CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i min.in -o min.out -p $prmtop -c $inpcrd -r min.rst -ref $inpcrd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i nvt.in -o nvt.out -p $prmtop -c min.rst -r heat.rst -ref min.rst -x heat.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i npt.in -o npt.out -p $prmtop -c heat.rst -r density.rst -ref heat.rst -x density.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i equil.in -o equil.out -p $prmtop -c density.rst -r equil.rst -ref density.rst -x equil.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i md_pre.in -o md_pre.out -p $prmtop -c equil.rst -r md_pre.rst -x md_pre.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i prod.in -o md.out -p md.prmtop -c md_pre.rst -r md.rst -x md.dcd