

## install Gaussian
### install gaosi16-A03-AVX2.tbz in Linux system
```
tar -xjvf gaosi16-A03-AVX2.tbz
cd g16
mkdir src
csh ./bsd/install

edit ~/.bashrc

export PATH=$PATH:/data/softwares/g16
export g16root=/data/softwares/g16
export PATH=$PATH:$g16root/bsd
source $g16root/bsd/g16.profile
export GAUSS_EXEDIR=$g16root
export GAUSS_SCRDIR=$g16root/src

```

### install Gaussian16win in Linux system
must install Gaussian and install GaussView next, and install GaussView at same directory as Gaussian
```
%chk=Fulvestrant.chk
%mem=16GB
%nprocshared=16
# opt B3LYP/6-31G(d) freq geom=connectivity

Fulvestrant

0 1
!!!... your coordinates, need change!!!
```

## optimize molecular conformation by Gaussian
### use GaussView to generate com or gjf input file
### run 
```
g16 < test.com > test.log
```
will generate test.chk file
### transform chk to fchk
```
formchk test.chk test.fchk
```
### transform fchk to mol2
```
sudo apt-get install openbabel
obabel -ifchk test.fchk -oxyz -O test.xyz
obabel -ixyz test.xyz -omol2 -O test.mol2
```
### other
Aufbau原则：电子先填充能量最低的轨道。
Pauli排斥原理：每个轨道最多可容纳两个自旋相反的电子。
Hund定则：在能量相同的轨道中，电子会尽可能保持未成对，且具有相同自旋。

即
(1)每个亚轨道最多2个电子
(2)在填充具有相同能量的亚轨道时，电子首先会单独占据各个轨道，并且具有相同的自旋方向，即只有当每个等能轨道都至少有一个电子后，电子才会开始成对
(3)任何两个电子不能占据同一个量子态，因此一个轨道最多只能容纳两个自旋相反的电子，即亚轨道电子成对自旋相反



