```
antechamber -fi mol2 -fo mol2 -i sitagplitin_init.mol2 -o sitagplitin.mol2 -c bcc -nc 0 -pf y -at gaff2 -m 1 -gm "%mem=4000MB" -gn "%nproc=2"
parmchk2 -i sitagplitin.mol2 -o sitagplitin.frcmod -f mol2

```
