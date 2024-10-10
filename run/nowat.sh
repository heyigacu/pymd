#!bin/bash
workdir=$(pwd)
num_residues=728
NO_ligand=729
echo $workdir

cat > $workdir/nowat_top.in << EOF
parm com_solv.prmtop
parmstrip :WAT,Na+,Cl-
parmbox nobox
parmwrite out nowat.prmtop
run

EOF

cat > $workdir/nowat_dcd.in << EOF
parm com_solv.prmtop
trajin ligamd_md.dcd
autoimage
strip :WAT,Na+,Cl-
trajout nowat.dcd
run

EOF

cpptraj -i nowat_top.in
cpptraj -i nowat_dcd.in
