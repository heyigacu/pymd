#!bin/bash
workdir=$(pwd)
num_residues=728
NO_ligand=729
Dis_A=729
Dis_B=592@CA
echo $workdir

cat > $workdir/analysis.in << EOF
parm nowat.prmtop
trajin nowat.dcd 1 -1 1
autoimage
rms :1-$num_residues@CA out rmsd.dat
run
radgyr :1-$num_residues@CA out rg.dat
run
rms first :1-$num_residues@CA
atomicfluct :1-$num_residues@CA out rmsf.dat
run
distance :$Dis_A :$Dis_B out dis.dat
run
secstruct :1-$num_residues out dssp.gnu
run
cluster c1 kmeans clusters 10 randompoint maxit 500 rms :1-$num_residues@C,N,O,CA,CB&!@H= sieve 10 random out cnumvtime.dat summary summary.dat info info.dat cpopvtime cpopvtime.agr normframe repout rep repfmt pdb singlerepout singlerep.nc singlerepfmt netcdf avgout avg avgfmt pdb
go

EOF

cat > $workdir/analysis_surf.in << EOF
parm nowat.prmtop
trajin nowat.dcd 1 -1 10
autoimage
surf :1-$num_residues out surf.dat
run

EOF


cpptraj -i analysis.in
cpptraj -i analysis_surf.in

