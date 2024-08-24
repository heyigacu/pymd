

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
```
must install Gaussian and install GaussView next, and install GaussView at same directory as Gaussian
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


