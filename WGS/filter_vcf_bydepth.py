###################################################################
# File Name: filter_vcf_bydepth.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年09月04日 星期一 13时29分58秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import argparse
'''This script was used to filter the vcf by the DP in Format Field'''
def filter_vcf_bydepth(vcf,output,dp):
	for line in vcf:
		if line.startswith("#"):
			output.write(line)
		else:
			tmps=line.rstrip().split("\t")
			if len(tmps)!=10:
				print("Please be careful about the vcf,it does not have 10 cols")
				exit(1)
			vcf_format,value=tmps[8:10]
			if vcf_format.find("DP")==-1:continue
			dp_index=vcf_format.split(":").index("DP")
			if int(value.split(":")[dp_index])>=dp:
				output.write(line)


def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-i','--input',help='The input vcf which included 10 cols',dest='vcf',required=True,type=open)
	parser.add_argument('-o','--output',help='the filter vcf',dest='output',required=True,type=argparse.FileType('w'))
	parser.add_argument('-dp','--depth',help='DP threshold for filter vcf',dest='dp',default=4,type=int)
	args=parser.parse_args()
	filter_vcf_bydepth(args.vcf,args.output,args.dp)

if __name__=="__main__":
	main()
