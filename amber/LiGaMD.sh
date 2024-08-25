
#!bin/bash
workdir=$(pwd)
cuda_device=0
num_residues=729
no_ligand=729
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

cat > $workdir/ligamd_pre.in << EOF
&cntrl
  imin=0, irest=0, ntx=1,
  ioutfm=1, nstlim=30000000,
  dt=0.002,
  tempi=310.0, temp0=310.0,
  ntc=2, ntf=1,
  ntt=3, gamma_ln=2.0,
  ntp=0, ntb=1, pres0=1.0, cut=8.0,
  iwrap = 1,
  ntr=0,
  ig=-1,
  ntpr=5000, ntwx=50000, ntwr=50000, ntwe=50000,

  igamd=11, irest_gamd=0,
  ntcmd=3000000, nteb=27000000, ntave=300000,
  ntcmdprep=900000, ntebprep=900000,
  sigma0P=6.0, sigma0D=6.0, iEP=2, iED=1,
  icfe=1, ifsc=1, gti_cpu_output=1, gti_add_sc=1,
  timask1=":$no_ligand", scmask1=":$no_ligand",
  timask2="", scmask2="",
  nlig=1, ibblig=1, atom_p=2472, atom_l=4, dblig=3.7,
/

EOF

cat > $workdir/prod.in << EOF
&cntrl
  imin=0, irest=1, ntx=5,
  ioutfm=1, nstlim=500000000,
  dt=0.002,
  tempi=310.0, temp0=310.0,
  ntc=2, ntf=1,
  ntt=3, gamma_ln=2.0,
  ntp=0, ntb=1, pres0=1.0, cut=8.0,
  iwrap = 1,
  ntr=0,
  ig=-1,
  ntpr=5000, ntwx=50000, ntwr=50000, ntwe=50000,

  igamd=11, irest_gamd=1,
  ntcmd=0, nteb=0, ntave=300000,
  ntcmdprep=0, ntebprep=0,
  sigma0P=6.0, sigma0D=6.0, iEP=2, iED=1,
  icfe=1, ifsc=1, gti_cpu_output=1, gti_add_sc=1,
  timask1=":$no_ligand", scmask1=":$no_ligand",
  timask2="", scmask2="",
  nlig=1, ibblig=1, atom_p=2472, atom_l=4, dblig=3.7,
/

EOF

CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i min.in -o min.out -p com_solv.prmtop -c com_solv.inpcrd -r min.rst -ref com_solv.inpcrd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i nvt.in -o nvt.out -p com_solv.prmtop -c min.rst -r heat.rst -ref min.rst -x heat.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i npt.in -o npt.out -p com_solv.prmtop -c heat.rst -r density.rst -ref heat.rst -x density.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i equil.in -o equil.out -p com_solv.prmtop -c density.rst -r equil.rst -ref density.rst -x equil.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i ligamd_pre.in -o ligamd_pre.out -p com_solv.prmtop -c equil.rst -r ligamd_pre.rst -x ligamd_pre.dcd
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i ligamd_pre.in -o ligamd_md.out -p com_solv.prmtop -c ligamd_pre.rst -r ligamd_md.rst -x ligamd_md.dcd


