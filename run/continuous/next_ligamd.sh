#!bin/bash
workdir=$(pwd)
cuda_device=1
num_residues=729
no_ligand=729
echo $workdir

cat > $workdir/ligamd_md_next.in << EOF
&cntrl
  imin=0, irest=1, ntx=5,
  ioutfm=1, nstlim=2500000,
  dt=0.002,
  tempi=310.0, temp0=310.0,
  ntc=2, ntf=1,
  ntt=3, gamma_ln=5.0,
  ntp=0, ntb=1, pres0=1.0, cut=8.0,
  iwrap = 1,
  ntr=0, 
  ig=-1,
  ntpr=5000, ntwx=50000, ntwr=50000, ntwe=50000,

  igamd=11, irest_gamd=1,
  ntcmd=0, nteb=0, ntave=300000,
  ntcmdprep=0, ntebprep=0,
  sigma0P=0.5, sigma0D=6.0, iEP=2, iED=1,
  icfe=1, ifsc=1, gti_cpu_output=0, gti_add_sc=1,
  timask1=":$no_ligand", scmask1=":$no_ligand",
  timask2="", scmask2="",
  nlig=1, ibblig=1, atom_p=9568, atom_l=50, dblig=3.7,
/

EOF

cp mdinfo mdinfo_backup
cp gamd.log gamd_backup.log
CUDA_VISIBLE_DEVICES=$cuda_device pmemd.cuda -O -i ligamd_md_next.in -o ligamd_md_next.out -p com_solv.prmtop -c ligamd_md.rst -r ligamd_md_next.rst -x ligamd_md_next.dcd