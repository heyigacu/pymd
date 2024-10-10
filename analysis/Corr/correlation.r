library("bio3d")

mydcdfile<-"nowat.dcd"
mypdbfile<-"dpp4.pdb" 
pdb<-read.pdb(mypdbfile)
dcd<-read.dcd(mydcdfile)

ca.inds <- atom.select(pdb, elety="CA")
xyz<-fit.xyz(fixed=pdb$xyz, mobile=dcd, fixed.inds=ca.inds$xyz,mobile.inds=ca.inds$xyz)
dim(xyz) == dim(dcd)
# plot co-variance
png(filename = "dccm.png",width = 18, height = 18,units = "cm",bg = "white",res = 300)
cij <- dccm(xyz[,ca.inds$xyz])
plot(cij)
dev.off()
# plot pca
png(filename = "pca.png",width = 18, height = 18,units = "cm",bg = "white",res =300)
pc <- pca.xyz(xyz[,ca.inds$xyz])
plot(pc, col=bwr.colors(nrow(xyz)))
dev.off()
