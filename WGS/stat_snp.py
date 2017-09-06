###################################################################
# File Name: stat_snp.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年09月05日 星期二 16时25分33秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import argparse
'''This script was used to stat the snp'''
def read_table(table):
	func={}
	exonic_func={}
	for line in table:
		tmps=line.strip().split("\t")
		if tmps[0]=="Chr" and tmps[1]=="Start":
			Fun_index=tmps.index("Func.refGene")
			ExonicFunc_index=tmps.index("ExonicFunc.refGene")
		else:
			if tmps[Fun_index] not in func:
				func[tmps[Fun_index]]=1
			else:
				func[tmps[Fun_index]]+=1
			if tmps[Fun_index]=="exonic":
				if tmps[ExonicFunc_index] not in exonic_func:
					exonic_func[tmps[ExonicFunc_index]]=1
				else:
					exonic_func[tmps[ExonicFunc_index]]+=1
	return func,exonic_func

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
	parser.add_argument('-o1','--output1',help="The snp Function discribution",dest="output1",required=True)
	parser.add_argument('-o2','--output2',help="The exonic snp Function discribution",dest="output2",required=True)
	parser.add_argument('-s','--sample',help="The sample name",dest="sample",required=True)
	args=parser.parse_args()
	func,exonic_func=read_table(args.input)
	dict_print(func,args.sample,args.output1)
	dict_print(exonic_func,args.sample,args.output2)

if __name__=="__main__":
	main()
