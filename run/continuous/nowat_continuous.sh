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

cat > $workdir/nowat_pre.in << EOF
parm com_solv.prmtop
trajin ligamd_md.dcd
autoimage
strip :WAT,Na+,Cl-
trajout nowat_pre.dcd
run

EOF

cat > $workdir/nowat_next.in << EOF
parm com_solv.prmtop
trajin ligamd_md_next.dcd
autoimage
strip :WAT,Na+,Cl-
trajout nowat_next.dcd
run

EOF


cpptraj -i nowat_top.in
cpptraj -i nowat_pre.in
cpptraj -i nowat_next.in
