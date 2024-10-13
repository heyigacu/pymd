
# pymd
a set of python tools for molecular dynamics
## 1.Prepare

### 1.1

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



## Run

## Analysis

## others
other tools

