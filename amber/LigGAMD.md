
## install amber
```
tar xvfj AmberTools24.tar.bz2
tar xvfj Amber24.tar.bz2
cd amber24_src/build # set DCUDA to TRUE for Linux
./run_cmake
make install -j 24
```

## LiGaMD
```
LiGaMD {
    If (irest_gamd == 0) then
        For i = 1, ..., ntcmd // run initial conventional molecular dynamics
            If (i >= ntcmdprep) Update Vmax, Vmin
            If (i >= ntcmdprep && i%ntave ==0) Update Vavg, sigmaV
        End
        Save Vmax,Vmin,Vavg,sigmaV to gamd_restart.dat file
        Calc_E_k0(iE,sigma0,Vmax,Vmin,Vavg,sigmaV)
        For i = ntcmd+1, ..., ntcmd+nteb // Run biasing molecular dynamics simulation steps
            deltaV = 0.5*k0*(E-V)**2/(Vmax-Vmin)
            V = V + deltaV
            If (i >= ntcmd+ntebprep) Update Vmax, Vmin
            If (i >= ntcmd+ntebprep && i%ntave ==0) Update Vavg, sigmaV
            Calc_E_k0(iE,sigma0,Vmax,Vmin,Vavg,sigmaV)
        End
        Save Vmax,Vmin,Vavg,sigmaV to gamd_restart.dat file
    else if (irest_gamd == 1) then
        Read Vmax,Vmin,Vavg, sigmaV from gamd_restart.dat file
    End if
    
    lig0=1 // ID of the bound ligand
        For i = ntcmd+nteb+1, ..., nstlim // run production simulation
            If (ibblig>0 && i%ntave ==0) then // swap the bound ligand with lig0 for selective boost
            For ilig = 1, ..., nlig
                dlig = distance(atom_p, atom_l)
                If (dlig <= dblig) blig=ilig
            End
            If (blig != lig0) Swap atomic coordinates, forces and velocities of ligands blig with lig0
        End if
        deltaV = 0.5*k0*(E-V)**2/(Vmax-Vmin)
        V = V + deltaV
    End
 }
```

## prepare
```
source /opt/amber/amber24/amber.sh
```

###ligand
#### add H to ligand in PyMOL or DS
```
antechamber -fi pdb -fo mol2 -i lig.pdb -o lig.mol2  -c bcc
parmchk2 -i lig.mol2 -o lig.frcmod -f mol2
```

####DPP4
```
pdb4amber -i rec.pdb -o rec_H.pdb --reduce
```

###tleap
```
source leaprc.protein.ff19SB
source leaprc.gaff2
source leaprc.water.opc
loadamberparams frcmod.ionslm_126_opc
loadamberparams lig.frcmod

lig = loadmol2 lig.mol2
rec_H = loadpdb rec_H.pdb

com = combine{rec_H,lig}
savepdb com com_dry.pdb
saveamberparm com com_dry.prmtop com_dry.inpcrd
solvatebox com OPCBOX 12.0
addions com Na+ 0
addions com Cl- 0
savepdb com com_solv.pdb
saveamberparm com com_solv.prmtop com_solv.inpcrd
quit
```
## run
### min.in
```
minimise
 &cntrl
  imin=1, maxcyc=2000, ncyc=100,
  ntc=1, ntf=1,
  ntp=0, ntb=1, cut=8.0,
  ntpr=100, ntwr=100,
  ntr=1, restraintmask=':1-729',
  restraint_wt=2.0
 /

```
### nvt.in
```
heat NVT 200ps
&cntrl
  imin=0, irest=0, ntx=1,
  nstlim=100000, dt=0.002,
  ntc=2, ntf=2, 
  ntt=3, gamma_ln=2.0,
  ntp=0, ntb=1, cut=8.0,
  ntr=1, restraintmask=':1-729', restraint_wt=1.0,
  tempi=0.0, temp0=300.0,
  iwrap=1,
  ig=-1,
  ntpr=1000, ntwx=1000, ntwr=10000,
/

&wt type='TEMP0', istep1=0, istep2=10000, value1=0.0, value2=300.0, &end
&wt type='END', &end

```
### npt.in
```
density NPT 200ps
&cntrl
  imin=0, irest=1, ntx=5,
  nstlim=100000, dt=0.002,
  ntc=2, ntf=2,
  ntt=3, gamma_ln=2.0,
  ntp=1, ntb=2, pres0=1.0, cut=8.0, taup=2.0,
  ntr=1, restraintmask=':1-729', restraint_wt=1.0,
  iwrap=1,
  ig=-1,
  tempi=310.0, temp0=310.0,
  ntpr=1000, ntwx=1000, ntwr=10000,
/

```
### equil.in
```
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

```
### ligamd_pre.in
```
&cntrl
  imin=0, irest=0, ntx=1,
  ioutfm=1, nstlim=26000000,
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
  ntcmd=2000000, nteb=24000000, ntave=400000,
  ntcmdprep=800000, ntebprep=800000,
  sigma0P=6.0, sigma0D=6.0, iEP=2, iED=1,
  icfe=1, ifsc=1, gti_cpu_output=1, gti_add_sc=1,
  timask1=":729", scmask1=":729",
  timask2="", scmask2="",
  nlig=1,  ibblig=1, atom_p=2472, atom_l=4, dblig = 3.7,
/

```

### ligamd_md.in
```
&cntrl
  imin=0, irest=1, ntx=5,
  ioutfm=1, nstlim=26000000,
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
  ntcmd=2000000, nteb=24000000, ntave=400000,
  ntcmdprep=800000, ntebprep=800000,
  sigma0P=6.0, sigma0D=6.0, iEP=2, iED=1,
  icfe=1, ifsc=1, gti_cpu_output=1, gti_add_sc=1,
  timask1=":729", scmask1=":729",
  timask2="", scmask2="",
  nlig=1,  ibblig=1, atom_p=2472, atom_l=4, dblig = 3.7,
/

```



### run
```
CUDA_VISIBLE_DEVICES=7 pmemd.cuda -O -i min.in -o min.out -p com_solv.prmtop -c com_solv.inpcrd -r min.rst -ref com_solv.inpcrd
CUDA_VISIBLE_DEVICES=7 pmemd.cuda -O -i nvt.in -o nvt.out -p com_solv.prmtop -c min.rst -r heat.rst -ref min.rst -x heat.dcd
CUDA_VISIBLE_DEVICES=7 pmemd.cuda -O -i npt.in -o npt.out -p com_solv.prmtop -c heat.rst -r density.rst -ref heat.rst -x density.dcd
CUDA_VISIBLE_DEVICES=7 pmemd.cuda -O -i equil.in -o equil.out -p com_solv.prmtop -c density.rst -r equil.rst -ref density.rst -x equil.dcd
CUDA_VISIBLE_DEVICES=7 pmemd.cuda -O -i ligamd_pre.in -o ligamd_pre.out -p com_solv.prmtop -c equil.rst -r ligamd_pre.rst -x ligamd_pre.dcd
CUDA_VISIBLE_DEVICES=7 pmemd.cuda -O -i ligamd_pre.in -o ligamd_md.out -p com_solv.prmtop -c ligamd_pre.rst -r ligamd_md.rst -x ligamd_md.dcd

```

## restart
```
mdin -c <your_restart_file.rst> -o output_file.out -r new_restart_file.rst -x trajectory_file.nc -inf mdinfo
```
change irest=1 and ntx=5, and nstlim to remain steps
```
CUDA_VISIBLE_DEVICES=7 pmemd.cuda -O -i mdin -o mdout_restart.out -p prmtop -c restart_file.rst -r new_restart.rst -x traj_restart.nc -inf mdinfo_restart
```

