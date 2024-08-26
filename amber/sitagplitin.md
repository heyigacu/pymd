# sitagliptin
```
antechamber -fi mol2 -fo mol2 -i sitagliptin_init.mol2 -o sitagliptin.mol2 -c bcc -nc 0 -pf y -at gaff2 -m 1 -gm "%mem=4000MB" -gn "%nproc=2"
parmchk2 -i sitagliptin.mol2 -o sitagliptin.frcmod -f mol2 -s gaff2

pdb4amber -i dpp4.pdb -o dpp4_H.pdb --reduce

source leaprc.protein.ff19SB
source leaprc.gaff2
source leaprc.water.opc
loadamberparams frcmod.ionslm_126_opc
loadamberparams sitagliptin.frcmod

sitagliptin = loadmol2 sitagliptin.mol2
rec_H = loadpdb dpp4_H.pdb

com = combine{rec_H,sitagliptin}
savepdb com com_dry.pdb
saveamberparm com com_dry.prmtop com_dry.inpcrd
solvatebox com OPCBOX 10.0
addions com Na+ 0
addions com Cl- 0
savepdb com com_solv.pdb
saveamberparm com com_solv.prmtop com_solv.inpcrd
quit

```


# lsavuconazonium
```
antechamber -fi mol2 -fo mol2 -i lsavuconazonium_init.mol2 -o lsavuconazonium.mol2 -c bcc -nc 0 -pf y -at gaff2 -m 2 -gm "%mem=8000MB" -gn "%nproc=4"
parmchk2 -i lsavuconazonium.mol2 -o lsavuconazonium.frcmod -f mol2 -s gaff2

pdb4amber -i dpp4.pdb -o dpp4_H.pdb --reduce

source leaprc.protein.ff19SB
source leaprc.gaff2
source leaprc.water.opc
loadamberparams frcmod.ionslm_126_opc
loadamberparams lsavuconazonium.frcmod

lsavuconazonium = loadmol2 lsavuconazonium.mol2
rec_H = loadpdb dpp4_H.pdb

com = combine{rec_H,lsavuconazonium}
savepdb com com_dry.pdb
saveamberparm com com_dry.prmtop com_dry.inpcrd
solvatebox com OPCBOX 10.0
addions com Na+ 0
addions com Cl- 0
savepdb com com_solv.pdb
saveamberparm com com_solv.prmtop com_solv.inpcrd
quit


```

# apo
```

pdb4amber -i dpp4.pdb -o dpp4_H.pdb --reduce

source leaprc.protein.ff19SB
source leaprc.water.opc
loadamberparams frcmod.ionslm_126_opc


com = loadpdb dpp4_H.pdb
savepdb com com_dry.pdb
saveamberparm com com_dry.prmtop com_dry.inpcrd
solvatebox com OPCBOX 10.0
addions com Na+ 0
addions com Cl- 0
savepdb com com_solv.pdb
saveamberparm com com_solv.prmtop com_solv.inpcrd
quit


```

# fulvestrant
```
antechamber -fi mol2 -fo mol2 -i fulvestrant_init.mol2 -o fulvestrant.mol2 -c bcc -nc 0 -pf y -at gaff2 -m 1 -gm "%mem=8000MB" -gn "%nproc=4"
parmchk2 -i fulvestrant.mol2 -o fulvestrant.frcmod -f mol2 -s gaff2

pdb4amber -i dpp4.pdb -o dpp4_H.pdb --reduce

source leaprc.protein.ff19SB
source leaprc.gaff2
source leaprc.water.opc
loadamberparams frcmod.ionslm_126_opc
loadamberparams fulvestrant.frcmod

fulvestrant = loadmol2 fulvestrant.mol2
rec_H = loadpdb dpp4_H.pdb

com = combine{rec_H,fulvestrant}
savepdb com com_dry.pdb
saveamberparm com com_dry.prmtop com_dry.inpcrd
solvatebox com OPCBOX 10.0
addions com Na+ 0
addions com Cl- 0
savepdb com com_solv.pdb
saveamberparm com com_solv.prmtop com_solv.inpcrd
quit




```

