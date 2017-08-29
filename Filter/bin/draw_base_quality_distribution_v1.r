#!/usr/bin/Rscript
args=commandArgs(T)
if (length(args)<5){
	print("Rscript draw_base_quality_distribution_v1.r input_report output.pdf Read1_length Read1&Read2_length output2.pdf [sample_name]")
	q()
}
data<-read.table(args[1],header=F)
length1=as.numeric(args[3])
length2=as.numeric(args[4])
sum=data$V1+data$V2+data$V3+data$V4+data$V5+data$V6
rate<-c(data$V2/sum*100,data$V3/sum*100,data$V4/sum*100,data$V5/sum*100,data$V6/sum*100)
content_max=max(rate)  #得到最高的那条线
par(mar=c(2.5,2.5,2.5,0.25))
high=70
low=0
posi=length2*0.8
if (content_max>70){high=90}
pdf(args[2],w=8,h=6)
xais=seq(0,length2,30)
yais=seq(low,high,10)
plot(data$V1,data$V2/sum*100,type="l",bty="l",col="red",ylim=c(low,high),xlim=c(0,length(data$V1)),xlab="",ylab="",xaxt="n",yaxt="n")
points(data$V1,data$V2/sum*100,col="red",pch=20)
lines(data$V1,data$V3/sum*100,col="blue",lwd=1.5)
points(data$V1,data$V3/sum*100, col = "blue",pch=20)
lines(data$V1,data$V4/sum*100,col="green",lwd=1.5)
points(data$V1,data$V4/sum*100, col = "green",pch=20)
lines(data$V1,data$V5/sum*100,col="darkmagenta",lwd=1.5)
points(data$V1,data$V5/sum*100, col = "darkmagenta",pch=20)
lines(data$V1,data$V6/sum*100,col="turquoise4",lwd=1.5)
points(data$V1,data$V6/sum*100, col = "turquoise4",pch=20)
legend(posi,65, c("A%","T%","C%", "G%","N%"),lwd=1,cex=0.8,col = c("red","blue","green","darkmagenta","turquoise4"),bty="n")
if (length2>length1){abline(v=length1,lty=2,col="black")}
axis(side=1,xais,tcl=-0.2,labels=FALSE)
axis(side=2,yais,tcl=-0.2,labels=FALSE)
mtext(xais,side=1,las=1,at=xais,cex=0.8)
mtext(yais,side=2,las=1,at=yais,cex=0.8,line=0.5)
mtext("Position",side=1,line=1.5)
mtext("Percent(%)",side=2,line=2)
title(paste("Base Distribution of ",args[6],sep=''))
dev.off()

pdf(args[5],w=8,h=6)
yais=seq(0,40,10)
plot(data$V1,data$V7,type="l",bty="l",col="red",ylim=c(0,50),xlim=c(0,length(data$V1)),xlab="",ylab="",xaxt="n",yaxt="n")
if(length2>length1){abline(v=length1,lty=2,col="black")}
legend(posi,50,"mean_quality",lwd=1,cex=0.8,col="red",bty="n")
axis(side=1,xais,tcl=-0.2,labels=FALSE)
mtext(xais,side=1,las=1,at=xais,cex=0.8)
mtext("Position",side=1,line=1.5)
axis(side=2,yais,tcl=-0.2,labels=FALSE)
mtext(yais,side=2,las=1,at=yais,cex=0.8,line=0.5)
mtext("Quality",side=2,line=2)
title(paste("Mean Quality Distribution of ",args[6],sep=''))
dev.off()

