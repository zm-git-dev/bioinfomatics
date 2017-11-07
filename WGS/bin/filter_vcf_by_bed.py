###################################################################
# File Name: filter_vcf_by_bed.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年11月07日 星期二 09时06分40秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
'''This script was used to filter the vcf by the bed'''
import argparse
def get_capture_region(bed_input):
	dic={}
	for line in bed_input:
		if line.startswith("chr"):
			tmp=line.strip().split()
			if tmp[0] not in dic:
				dic[tmp[0]]={}
			for i in range(int(tmp[1]),int(tmp[2])+1):
				dic[tmp[0]][i]=""
	return dic

def filter_the_vcf(bed_input,vcf_input,output):
	dic=get_capture_region(bed_input)
	for line in vcf_input:
		if line.startswith("#"):
			output.write(line)
			continue
		tmps=line.strip().split("\t")
		if tmps[0] in dic and int(tmps[1]) in dic[tmps[0]]:
			output.write(line)
	output.close



def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-i','--input',help='The vcf need to be filtered',dest='vcf_input',required=True,type=open)
	parser.add_argument('-t',help='the bed of exon chip',dest='bed_input',required=True,type=open)
	parser.add_argument('-o','--output',help='the filtered vcf output',dest="output",required=True,type=argparse.FileType('w'))
	args=parser.parse_args()
	filter_the_vcf(args.bed_input,args.vcf_input,args.output)

if __name__=="__main__":
	main()
