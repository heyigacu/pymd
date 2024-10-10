program ddtpd  ! Convert dot distribution to probability distribution
implicit real*8 (a-h,o-z)

real*8,allocatable :: datax(:),datay(:)
real*8 :: minx,maxx,miny,maxy,minz=1000,maxz=-1000
logical alive
character filename*80,test*1,test10*10

write(*,*) "Convert dot distribution to probability distribution"
write(*,*) "Programmed by Sobereva, 2010-NOV-4, v1.3"
write(*,*) "Bug report or recommend please contact: sobereva@sina.com"
write(*,*) "Press Ctrl+C to exit"
write(*,*)
do while(.true.)
	write(*,*) "Input g_anaeig -2d result filename"
	read(*,*) filename
	inquire(file=filename,exist=alive)
	if (alive) exit
	write(*,*) "File not found, input again"
end do
open(10,file=filename,access="sequential",status="old")
numcom=0 !Number of comment lines
do while(.true.)
	read (10,"(a1)") test
	if (test/="@".and.test/="#") then
		backspace(10)
		exit
	end if
	numcom=numcom+1
end do
numdata=0
do while(.true.)
	read(10,"(a10)",iostat=ierror) test10
	if (test10=="          ".or.ierror/=0) exit
	numdata=numdata+1
end do
rewind(10)
allocate(datax(numdata),datay(numdata))
do i=1,numcom
	read(10,*)
end do
read(10,*) (datax(i),datay(i),i=1,numdata)
close(10)

minx=minval(datax)
maxx=maxval(datax)
miny=minval(datay)
maxy=maxval(datay)

write(*,*) "Total number of data is",numdata
write(*,"(a,f12.6,a,f12.6)") "Minimum of x is",minx," Maximum of x is",maxx
write(*,"(a,f12.6,a,f12.6)") "Minimum of y is",miny," Maximum of y is",maxy
write(*,*)
write(*,*) "Set number of grids"
write(*,*) "Input number of x"
read(*,*) numx
write(*,*) "Input number of y"
read(*,*) numy
write(*,*)
spacex=(maxx-minx)/(numx-1)
spacey=(maxy-miny)/(numy-1)
write(*,"(a,f12.6,a,f12.6)") "Space of x is",spacex, " Space of y is",spacey
write(*,*) "Which type of result you want?"
write(*,*) "Input 1 to select P"
write(*,*) "Input 2 to select -LnP"
write(*,*) "Input 3 to select P with gaussian broadening"
write(*,*) "Input 4 to select -LnP with gaussian broadening"
read(*,*) iresulttype
if (iresulttype==3.or.iresulttype==4) then
	write(*,*) "Input broadening scale, default is 1, the bigger the broaden range is larger"
	read(*,*) brdscale
end if
write(*,*) "If output the points with P=0? (y/n)"
read(*,*) test
ioutputzero=0
if (test=='y'.or.test=='Y') ioutputzero=1

open(11,file="result.txt",status="replace")
area=spacex*spacey
ioutnum=0
zeronlnP=-Dlog(1D-6)
critdissqr=(spacex**2+spacey**2)*brdscale**2
FWHM=sqrt(spacex**2+spacey**2)*brdscale
gauss_c=FWHM/2/sqrt(2*dlog(2D0))
gauss_norm=(1/(gauss_c*sqrt(2*3.14159265358979324D0)))**2
gauss_exp=-1/(2*gauss_c**2)
do ix=1,numx
	do iy=1,numy
		flowx=minx+(ix-1)*spacex
		fhighx=flowx+spacex
		flowy=miny+(iy-1)*spacey
		fhighy=flowy+spacey
		fnowcenx=flowx+spacex/2
		fnowceny=flowy+spacey/2
		tempnum=0 !Number of point in this minival square area
		if (iresulttype==1.or.iresulttype==2) then
			do i=1,numdata
				if (datax(i)>=flowx.and.datax(i)<fhighx.and.datay(i)>=flowy.and.datay(i)<fhighy) tempnum=tempnum+1D0
			end do
		else if (iresulttype==3.or.iresulttype==4) then !Broadening points
			do i=1,numdata
				r2=(datax(i)-fnowcenx)**2+(datay(i)-fnowceny)**2
		! Gaussian function not equals to zero, so we cut the function, if distance exceed FWHM,
		! the function already become very small and can be safely ignored.
				if (r2>critdissqr) cycle
				tempnum=tempnum+gauss_norm*dexp(r2*gauss_exp)
			end do		
		end if
		P=tempnum/numdata/area
		if (tempnum==0) then
			if (ioutputzero==0) cycle
			if (iresulttype==1.or.iresulttype==3) z=P
			if (iresulttype==2.or.iresulttype==4) z=zeronlnP !An arbituary setting
		else
			if (iresulttype==1.or.iresulttype==3) z=P
			if (iresulttype==2.or.iresulttype==4) z=-Dlog(P)
		end if
		if (P/=0D0.and.z>maxz) maxz=z
		if (P/=0D0.and.z<minz) minz=z
		write(11,"(3f12.6)") fnowcenx,fnowceny,z
		ioutnum=ioutnum+1
	end do
end do
close(11)

write(*,"(a,f12.6)") "Minimum value is",minz
write(*,"(a,f12.6)") "Maximum value is",maxz
write(*,"(a,i10)") "The number of points outputted is",ioutnum
if ((iresulttype==2.or.iresulttype==4).and.ioutputzero==1) write(*,"(' In result.txt,',f12.6,' means P=0 in this minival area')") zeronlnP
write(*,*) "Result have been saved to result.txt in current directory"

if (iresulttype==2.or.iresulttype==4) then
	write(*,"(' If set ',f12.6,' as G=0? (y/n)')") minz
	read(*,*) test
	if (test=="y") then
		open(11,file="result.txt",access="sequential",status="old")
		open(12,file="result2.txt",status="replace")
		do while(.true.)
			read(11,*,iostat=ierror) tmpx,tmpy,tmpz
			if (ierror/=0) exit
			tmpz=tmpz-minz
			write(12,"(3f12.6)") tmpx,tmpy,tmpz
		end do
		close(11)
		close(12)
	write(*,"(a,f12.6)") "Now minimum result is",minz-minz
	write(*,"(a,f12.6)") "Now maximum result is",maxz-minz
	if (ioutputzero==1) write(*,"(' In result2.txt,',f12.6,' means P=0 in this minival area')") zeronlnP-minz
	write(*,*) "Aligned result have been saved to result2.txt in current directory"
	end if
end if

write(*,*) "Press Enter to exit"
read(*,*)
end