###################################################################
# File Name: FQ_QC.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年08月03日 星期四 13时28分39秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import argparse
import gzip
import os
'''This script was used to get the clean data by PE reads'''

###################caculate the rate of N#######################

def N_percent(seq,N_rate):
	real_N_rate=seq.count(b"N")/len(seq)
	if real_N_rate>N_rate:
		return False
	else:
		return True

##################get the phred score#########################

def get_phred(Ass,phred):
	return Ass-phred

#################get the rate of low_quality##################

def low_qulity(seq,quality,low_rate,phred): 
	tag=0
	for letter in seq:
		if get_phred(letter,phred)<=quality:
			tag+=1
	if tag/len(seq)>low_rate:
		#print(tag/len(seq))
		return False
	else:
		return True
###################read_adapter###################################
def read_adapter(adapter):
	adap={}
	with gzip.open(adapter,"rb") as f:
		for line in f:
			temp=line.strip().split(b"\t")
			temp[0]=b"@"+temp[0]
			adap[temp[0]]=""
	return adap

################################################################
def main():
	parser=argparse.ArgumentParser(description=__doc__)
	parser.add_argument('-i1','--input1',help="The Read1 fastq.gz. if not PE Sequencing,choose it", dest='R1',required=True)
	parser.add_argument('-i2','--input2',help="The Read2 fastq.gz. if not PE Sequencing,ignore it",dest='R2',required=False)
	parser.add_argument('-o1','--output1',help="The Read1 fqstq.gz which was clean data. If not PE Sequencing,choose it",dest='out_R1',required=True)
	parser.add_argument('-o2','--output2',help="The Read2 fastq.gz which was clean data. if not PE Sequencing,ignore it",dest='out_R2',required=False)
	parser.add_argument('-n','--n_rate',help="The rate of N, default=0.05",dest='n_rate',default="0.05",type=float)
	parser.add_argument('-q','--quality',help="under the  phred score need be calulatedi,default=19",dest='quality',default=19,type=int)
	parser.add_argument('-l','--low_rate',help="the max rate of low quality base in a read,default=0.15",dest="low_rate",default=0.15,type=float)
	parser.add_argument('-phred',help="The phred score, 33 or 64,default=33",dest='phred',default=33,type=int)
	options=parser.parse_args()

	if options.R2:
		print("PE ok")
		adapter_num=0
		adapter_record=open(os.path.dirname(options.out_R1)+"/adapter.txt","w")
		output1=gzip.open(options.out_R1,"wb")
		output2=gzip.open(options.out_R2,"wb")
		adapter1={}
		adapter2={}
		if (os.path.exists(options.R1+".adapter.gz")):
			adapter1=read_adapter(options.R1+".adapter.gz")
		else:
			raise Exception(options.R1+".adapter.gz"+"\tdid not exist")
		if (os.path.exists(options.R2+".adapter.gz")):
			adapter2=read_adapter(options.R2+".adapter.gz")
		else:
			raise Exception(options.R2+".adapter.gz"+"\tdid not exist")
		with gzip.open(options.R1,"rb") as f1,gzip.open(options.R2,"rb") as f2:
			for x,y in zip(f1,f2):
				fq1_reads=next(f1).rstrip()
				fq2_reads=next(f2).rstrip()
				fq1_plus=next(f1)
				fq2_plus=next(f2)
				fq1_value=next(f1).rstrip()
				fq2_value=next(f2).rstrip()
				if x.strip() in adapter1:
					adapter_num+=1
					continue
				if y.strip() in adapter2:
					adapter_num+=1
					continue
				if N_percent(fq1_reads,options.n_rate) and low_qulity(fq1_value,options.quality,options.low_rate,options.phred):
					if N_percent(fq2_reads,options.n_rate) and low_qulity(fq2_value,options.quality,options.low_rate,options.phred):
							output1.write(x+fq1_reads+b"\n"+fq1_plus+fq1_value+b"\n")
							output2.write(y+fq2_reads+b"\n"+fq2_plus+fq2_value+b"\n")
		adapter_record.write(str(adapter_num)+"\n")
		adapter_record.close()
	else:
		print("single ok")
		adapter_record=open(os.path.dirname(options.out_R1)+"/adapter.txt","w")
		adapter1={}
		if (os.path.exists(options.R1+".adapter.gz")):
			adapter1=read_adapter(options.R1+".adapter.gz")
		else:
			raise Exception(options.R1+".adapter.gz"+"\tdid not exist")
		output1=gzip.open(options.out_R1,"wb")
		with gzip.open(options.R1,"rb") as f1:
			for x in f1:
				fq1_reads=next(f1).rstrip()
				fq1_plus=next(f1)
				fq1_value=next(f1).rstrip()
				if x.strip() in adapter1:
					adapter_num+=1
					continue
				if N_percent(fq1_reads,options.n_rate) and low_qulity(fq1_value,options.quality,options.low_rate,options.phred):
					output1.write(x+fq1_reads+b"\n"+fq1_plus+fq1_value+b"\n")
		adapter_record.write(str(adapter_num)+"\n")
		adapter_record.close()
		
if __name__=="__main__":
	main()

	
	
	
