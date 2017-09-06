###################################################################
# File Name: stat_snp.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年09月05日 星期二 16时25分33秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import argparse
from itertools import permutations
'''This script was used to stat the snp'''
def read_table(table):
	func={}
	exonic_func={}
	change_type={}
	exonic_change_type={}
	snp_change=["A","T","C","G"]
	for j in permutations(snp_change,2):
		exonic_change_type["".join(list(j))]=0
		change_type["".join(list(j))]=0
	for line in table:
		tmps=line.strip().split("\t")
		if tmps[0]=="Chr" and tmps[1]=="Start":
			Fun_index=tmps.index("Func.refGene")
			ExonicFunc_index=tmps.index("ExonicFunc.refGene")
			Ref_index=tmps.index("Ref")
			Alt_index=tmps.index("Alt")
		else:
			if len(tmps[Ref_index])!=1 or len(tmps[Alt_index])!=1:
				print("Please check snp in this line"+"\t"+line)
				exit(1)
			Ref_Alt=tmps[Ref_index]+tmps[Alt_index]
			change_type[Ref_Alt]+=1
			if tmps[Fun_index] not in func:
				func[tmps[Fun_index]]=1
			else:
				func[tmps[Fun_index]]+=1
			if tmps[Fun_index]=="exonic":
				exonic_change_type[Ref_Alt]+=1
				if tmps[ExonicFunc_index] not in exonic_func:
					exonic_func[tmps[ExonicFunc_index]]=1
				else:
					exonic_func[tmps[ExonicFunc_index]]+=1
	return func,exonic_func,change_type,exonic_change_type

def dict_print(dic,name,output):
	ff=open(output,"w")
	order=sorted(dic.keys())
	line1="Sample"+"\t"+"\t".join(order)
	line2=name
	for i in order:
		line2=line2+"\t"+str(dic[i])
	ff.write(line1+"\n")
	ff.write(line2+"\n")
	ff.close()

def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-i','--input',help="The snp multianno", dest='input',required=True,type=open)
	parser.add_argument('-o1','--output1',help="The snp Function distribution",dest="output1",required=True)
	parser.add_argument('-o2','--output2',help="The exonic snp Function distribution",dest="output2",required=True)
	parser.add_argument('-o3','--output3',help="The tv/ts distribution",dest="output3",required=True)
	parser.add_argument('-o4','--output4',help="The snp change type",dest="output4",required=True)
	parser.add_argument('-s','--sample',help="The sample name",dest="sample",required=True)
	args=parser.parse_args()
	func,exonic_func,genome_type,exonic_type=read_table(args.input)
	tv_ts=open(args.output3,"w")
	snp_change=open(args.output4,"w")
	genome_tv=genome_type["CA"]+genome_type["CT"]+genome_type["AC"]+genome_type["TC"]+genome_type["GT"]+genome_type["GA"]+genome_type["TG"]+genome_type["AG"]
	exonic_tv=exonic_type["CA"]+exonic_type["CT"]+exonic_type["AC"]+exonic_type["TC"]+exonic_type["GT"]+exonic_type["GA"]+exonic_type["TG"]+exonic_type["AG"]
	genome_ts=genome_type["CG"]+genome_type["AT"]+genome_type["GC"]+genome_type["TA"]
	exonic_ts=exonic_type["CG"]+exonic_type["AT"]+exonic_type["GC"]+exonic_type["TA"]
	genome_ts_tv="%.4f" % (genome_ts/genome_tv)
	exonic_ts_tv="%.4f" % (exonic_ts/exonic_tv)
	tv_ts.write("Sample\tTs genome\tTv genome\tTs/Tv genome\tTs exonic\tTv exonic\tTs/Tv exonic\n")
	tv_ts.write("{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n".format(args.sample,genome_ts,genome_tv,genome_ts_tv,exonic_ts,exonic_tv,exonic_ts_tv))
	tv_ts.close()
	snp_change.write("Sample\t{0}\n".format(args.sample))
	snp_change.write("C-G\t{0}\n".format(genome_type["CG"]+genome_type["GC"]))
	snp_change.write("C-A\t{0}\n".format(genome_type["CA"]+genome_type["GT"]))
	snp_change.write("C-T\t{0}\n".format(genome_type["CT"]+genome_type["GA"]))
	snp_change.write("A-T\t{0}\n".format(genome_type["AT"]+genome_type["TA"]))
	snp_change.write("A-G\t{0}\n".format(genome_type["AG"]+genome_type["TC"]))
	snp_change.write("A-C\t{0}\n".format(genome_type["AC"]+genome_type["TG"]))
	snp_change.close()
	dict_print(func,args.sample,args.output1)
	dict_print(exonic_func,args.sample,args.output2)

if __name__=="__main__":
	main()
