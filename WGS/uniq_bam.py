###################################################################
# File Name: uniq_bam.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年08月11日 星期五 15时08分18秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import argparse
'''This script was used to get the uniq bam and record the bam'''
#########################判断该序列是否是次优的比对结果##############################################
def best_hit(num):
	hit_score=bin(int(num))
	if len(hit_score)>=9:
		if hit_score[-9]=="1":
			return False
		else:
			return True
	else:
		return True

###################################################################################################
def read_sam(insam,outsam,stat):
	out=open(outsam,"w")
	statout=open(stat,"w")
	map_count=0
	uniq_map=0
	with open(insam) as f:
		for line in f:
			if line.startswith("@"):
				out.write(line)
				continue
			map_count+=1
			tmps=line.strip().split("\t")
			if best_hit(tmps[1]):
				out.write(line)
				uniq_map+=1
	statout.write("Map counts:\t"+str(map_count)+"\n")
	statout.write("Uniq map_reads:\t"+str(uniq_map)+"\n")
	rate=uniq_map/map_count
	statout.write("Uniq mapping rate:\t"+str(rate)+"\n")


def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-i','--in',help='the sam which has been filtered the unmapping reads',dest='insam',required=True)
	parser.add_argument('-o','--out',help='the sam which filtered the second best mapping reads',dest='outsam',required=True)
	parser.add_argument('-s','--stat',help='the stat of uniq mapping reads',dest='stat',required=True)
	args=parser.parse_args()
	read_sam(args.insam,args.outsam,args.stat)

if __name__=="__main__":
	main()
			
	
			
	
