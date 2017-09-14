###################################################################
# File Name: stat_depth_coverage.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年08月14日 星期一 13时50分46秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import argparse 
'''This script was used to caculate the depth and coverage'''
def genome_size(genome): #fasta
	size_len=0
	for line in genome:
		line=line.strip()
		if line.startswith(">"):continue
		size_len+=len(line)
	return size_len
def read_depth(in_depth,length,out_stat):
	dic={}
	site=0
	flag=1 
	out=open(out_stat,"w") 
	sum_depth=0
	sum_more_one_depth=0
	with open(in_depth) as f:
		for line in f:
			site+=1
			tmps=line.strip().split("\t")
			tmps[2]=int(tmps[2])
			sum_depth+=tmps[2]
			if tmps[2] in dic:
				dic[tmps[2]]+=1;
			else:
				dic[tmps[2]]=1;
			if tmps[2]>=1: sum_more_one_depth+=1
	mean_depth=sum_depth/length
	mean_coverage=sum_more_one_depth/length
	tmp_value=length-site         #the unmap sites in the genome
	for key in sorted(dic.keys()):
		if key==0 and flag==1:
			tmp_value0=dic[key]+tmp_value
			out.write("0\t"+str(tmp_value0)+"\n")
			flag=0
		elif key!=0 and flag==1:
			out.write("0\t"+str(tmp_value)+"\n")
			out.write(str(key)+"\t"+str(dic[key])+"\n")
			flag=0
		else:
			out.write(str(key)+"\t"+str(dic[key])+"\n")
	out.write("平均深度为\t"+str(mean_depth)+"\n")
	out.write("平均覆盖度为\t"+str(mean_coverage)+"\n")
	out.close()

def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-i','--in_depth',help="The depth(samtools depth)", dest='in_depth',required=True)
	parser.add_argument('-g','--genome',help="the reference genome",dest='genome',required=True,type=open)
	parser.add_argument('-o','--out_stat',help="The stat of depth and coverage",dest='out_stat',required=True)
	args=parser.parse_args()
	read_depth(args.in_depth,genome_size(args.genome),args.out_stat)


if __name__=="__main__":
	main()
