###################################################################
# File Name: draw_base_quality_distribution_v1.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年08月07日 星期一 14时42分50秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import argparse
import os

bindir= os.path.abspath(os.path.dirname(__file__))

'''This script was use to generate a data for draw the base quality and distribution.'''
##########################get the mean of the phred#################################################################
def get_quality_mean(mylist):
	result=0
	num=0
	for i in range(len(mylist)):
		result+=i*int(mylist[i])
		num+=int(mylist[i])
	result=result/num
	return str(result)
###########################read the report of fq######################################################################
def read_report(report,output,base):
	for i in report:
		if i.startswith("#"):continue
		base+=1
		cols=i.rstrip().split("\t")
		bases=cols[1:6]
		quals=cols[6:]
		output.write(str(base)+"\t"+"\t".join(bases))
		output.write("\t"+get_quality_mean(quals)+"\n")
	return base

def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-r1','--report1',help="The report of Read1. If not PE Sequencing,only choose it,ingore r2", dest='R1',required=True,type=open)
	parser.add_argument('-r2','--report2',help="The report of Read2. if not PE Sequencing,ignore it",dest='R2',required=False,type=open)
	parser.add_argument('-s','--sample',help="The name of the sample",dest='sample',required=True)
	args=parser.parse_args()
	if args.R2:
		base=0
		with open(args.sample+".temp","w") as f:
			R2_base=read_report(args.R1,f,base)
			total_base=read_report(args.R2,f,R2_base)
		os.system("/usr/bin/Rscript {0}/draw_base_quality_distribution_v1.r {1} {2} {3} {4} {5} {6} && rm {1}".format(bindir,args.sample+".temp",args.sample+"_base.pdf",R2_base,total_base,args.sample+"_quality.pdf",os.path.basename(args.sample)))
	else:
		base=0
		with open(args.sample+".temp","w") as f:
			total_base=read_report(args.R1,f,base)
		os.system("/usr/bin/Rscript {0}/draw_base_quality_distribution_v1.r {1} {2} {3} {4} {5} {6} && rm {1}".format(bindir,args.sample+".temp",args.sample+"_base.pdf",total_base,total_base,args.sample+"_quality.pdf",os.path.basename(args.sample)))
				
if __name__=="__main__":
	main()
