
## optimize molecular conformation by Gaussian

### install gaosi16-A03-AVX2.tbz
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
