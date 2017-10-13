###################################################################
# File Name: capture_rate.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年10月12日 星期四 09时52分13秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import sys
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

	return dic

def get_capture_rate(bed_input,depth_input):
	target_base=0
	mapping_base=0
	target=get_capture_region(bed_input)
	for line in depth_input:
		tmps=line.strip().split()
		mapping_base+=int(tmps[2])
		if tmps[0] in target and int(tmps[1]) in target[tmps[0]]:
			target_base+=int(tmps[2])
			print (line.strip())
	rate=target_base/mapping_base
	return [target_base,mapping_base,rate]



def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-i','--input',help='Depth which used samtools',dest='depth_input',required=True,type=open)
	parser.add_argument('-t',help='the bed of exon chip',dest='bed_input',required=True,type=open)
	parser.add_argument('-o','--output',help='the table of results of capture rate',dest="output",required=True,type=argparse.FileType('w'))
	args=parser.parse_args()
	result=get_capture_rate(args.bed_input,args.depth_input)
	args.output.write("target_base\t"+str(result[0])+"\n")
	args.output.write("mapping_base\t"+str(result[1])+"\n")
	args.output.write("capture_rate\t"+str(result[2])+"\n")



if __name__=="__main__":
	main()


