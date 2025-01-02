
#!bin/bash
workdir=$(pwd)
cuda_device=0
num_residues=728
no_ligand=728
temperature=310.0
echo $workdir
md_steps=250000000


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



cat > $workdir/server23.slurm << \EOF
#!/bin/bash
#SBATCH --time=720:00:00   # walltime
#SBATCH --ntasks-per-node=1 # GPU only version
#SBATCH --nodes=1   # number of nodes
#SBATCH --gpus-per-node=1  # number of GPU
#SBATCH --gres=gpu:1
#SBATCH --mem=30G   # memory
#SBATCH -J "amber"   # job name


### Do no change anything bellow ....
userName=`whoami`

# LOAD MODULES, INSERT CODE, AND RUN YOUR PROGRAMS HERE
ulimit -d unlimited
ulimit -s unlimited
ulimit -t unlimited
ulimit -v unlimited

export SLURM_EXPORT_ENV=ALL
/usr/local/cuda-11.8/extras/demo_suite/deviceQuery


export EXE="singularity exec --nv /opt/hpc4you/apps/amber22/amber22-amberTools22-GPU-openMPI.EXE"



cd $SLURM_SUBMIT_DIR

echo "Starting Amber on: `hostname` at `date`" >> ${SLURM_JOB_ID}.log

# Launch Amber
# ${EXE} Your-Input-String-Here

# for example,

${EXE} pmemd.cuda -O -i min.in -o min.out -p com_solv.prmtop -c com_solv.inpcrd -r min.rst -ref com_solv.inpcrd
${EXE} pmemd.cuda -O -i nvt.in -o nvt.out -p com_solv.prmtop -c min.rst -r heat.rst -ref min.rst -x heat.dcd
${EXE} pmemd.cuda -O -i npt.in -o npt.out -p com_solv.prmtop -c heat.rst -r density.rst -ref heat.rst -x density.dcd
${EXE} pmemd.cuda -O -i equil.in -o equil.out -p com_solv.prmtop -c density.rst -r equil.rst -ref density.rst -x equil.dcd
${EXE} pmemd.cuda -O -i cmd.in -o cmd.out -p com_solv.prmtop -c equil.rst -r cmd.rst -x cmd.dcd


echo "Finished Amber on: `hostname` at `date`" >> ${SLURM_JOB_ID}.log
echo $SLURM_JOB_NODELIST >> ${SLURM_JOB_ID}.log


EOF


qsub server23.slurm


