#!bin/bash
workdir=$(pwd)
Emax=20
cutoff=10
binx=6
biny=6
binz=6
data_1d=rmsd.dat
data_2d=dis.dat
data_3d=dis.dat
T=310

echo $workdir

#awk 'NR%1==0' gamd.log | awk '{print ($8+$7)/(0.001987*$T)" " $2 " " ($8+$7)}' > weights.dat
#awk -v temp="$T" 'NR % 1 == 0 {print (($8 + $7) / (0.001987 * temp)) " " $2 " " ($8 + $7)}' gamd.log > weights.dat



bash analysis.sh
awk -v temp="$T" 'NR % 1 == 0 {print (($8 + $7) / (0.001987 * temp)) " " $2 " " ($8 + $7)}' gamd.log > weights.log
awk 'NR > 3' weights.log > weights.dat

awk 'NR > 1 {print $2}' rmsd.dat > rmsd_.dat
awk 'NR > 1 {print $2}' rg.dat > rg_.dat



./reweight-1d.sh $Emax $cutoff $binx $data_1d $T

./reweight-2d.sh $Emax $cutoff $binx $biny $data_2d $T
# ./reweight-2d.sh 60 10 0.1 0.1 rmsdrg.dat 310


./reweight-3d.sh $Emax $cutoff $binx $biny $binz $data_3d $T
