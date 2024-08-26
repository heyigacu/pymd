
### adt tools 
https://vina.scripps.edu/downloads/
### vina
https://ccsb.scripps.edu/mgltools/downloads/

## parepare config.txt
```
receptor = dpp4.pdbqt
ligand = ligand.pdbqt
center_x = 0.0
center_y = 0.0
center_z = 0.0
size_x = 10.0
size_y = 10.0
size_z = 10.0
out = ligand_out.pdbqt

```


####
```
python D:/mgltools/Lib/site-packages/AutoDockTools/Utilities24/prepare_ligand4.py -l Fulvestrant.mol2 -o Fulvestrant.pdbqt > Fulvestrant.log
python D:/mgltools/Lib/site-packages/AutoDockTools/Utilities24/prepare_ligand4.py -l Lsavuconazonium.mol2 -o Lsavuconazonium.pdbqt > Lsavuconazonium.log
python D:/mgltools/Lib/site-packages/AutoDockTools/Utilities24/prepare_ligand4.py -l Meropenem.mol2 -o Meropenem.pdbqt > Meropenem.log
python D:/mgltools/Lib/site-packages/AutoDockTools/Utilities24/prepare_ligand4.py -l Paliperidone.mol2 -o Paliperidone.pdbqt > Paliperidone.log

vina --config congfig_Fulvestrant.txt > Fulvestrant.log
vina --config congfig_Lsavuconazonium.txt > Lsavuconazonium.log
vina --config congfig_Meropenem.txt > Meropenem.log
vina --config congfig_Paliperidone.txt  > Paliperidone.log

```
