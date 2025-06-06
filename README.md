
# pymd
a set of python tools for molecular dynamics
## 1.Prepare

### 1.1 gausssian

#### charge
* At physiological pH, the side chains of Arg and His carry a +1 charge, with histidine protonated at the NE atom.

#### pre-optimization
First, you need to use [GaussView](https://gaussian.com/gaussview6/) to generate the `.gjf` coordinates, and replace the header section of the file with the following content.
```
%chk=DDHR_preopt.chk
%NProcShared=24
%Mem=96GB
# PM6 Opt SCRF=(PCM,Solvent=Water)

DDHR_preopt

-1 1
```
g16 < DDHR_preopt.gjf > DDHR_preopt.log
formchk DDHR_preopt.chk DDHR_preopt.fchk
```

```
then you will get DDHR_preopt.chk
```

```
#### production in water
```
%chk=DDHR.chk
%NProcShared=24
%Mem=96GB
# B3LYP/6-31G(d) Opt Freq SCRF=(PCM,Solvent=Water)

DDHR

-1 1
```



### 1.2 molecular dock for ligand-eceptor
#### 1.2.1 vina 

first you must install openbabel and vina, and set their path in prepare/dock/dock_vina.py,
then change parameters of function run_vina_and_extract_best() in prepare/dock/dock_vina.py:  
* task_name: task name for dock, recommended as '$protein_name-$ligand_name'
* vina_config_file: vina config.txt path
* repeat_times: vina repeat times, recommended 100
for example:
```
run_vina_and_extract_best(task_name='CXCL2-quercetin', vina_config_file='CXCL2-quercetin/config.txt', repeat_times=100,)
```
and then run prepare/dock/dock_vina.py  
finally will generate best mol2 of ligand for each dock (because each vina dock will generate default 9 dock poses for ligand) in $task_name/best_mol2/,  
and will generate score table including each dock in $task_name/best_scores.txt.

#### 1.2.2 cluster
change mol2_dir to mol2 directory generate by section 1.2.1 above in prepare/dock/cluster.py  
then run prepare/dock/cluster.py  
and will generate cluster figure in same directory of mol2_dir as cluster.png:
![clutser.png](/prepare/dock/cluster.png)
then input a cutoff value for cluster according to cluster.png  
final will generate run_?_best.mol2 as reprensentive structure of biggest cluster.


## Run

### cmd 

you can run below to get correct command and run it
```
bash submit_cmd.sh -h
```
if you use slurm, you can run below after altering parameters
```
bash submit_cmd_slurm.sh
```



## Analysis

### MMPBSA

for example, the ligand (peptide) is Residue 729-733, please modify gen_mmpbsa.py, and run below
```
python gen_mmpbsa.py
ante-MMPBSA.py -p nowat.prmtop -c com.prmtop -r rec.prmtop -l lig.prmtop -s ':WAT,Na+,Cl-' -n ':729-733' 
nohup MMPBSA.py -O -i mmpbsa.in -o MMPBSA.dat -sp nowat.prmtop -cp com.prmtop -rp rec.prmtop -lp lig.prmtop -y nowat.dcd &
```

## others
other tools

