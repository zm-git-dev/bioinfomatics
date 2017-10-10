###################################################################
# File Name: filter_v1.1.1.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年08月18日 星期五 13时44分30秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import os
import sys
import re
import argparse
bindir = os.path.abspath(os.path.dirname(__file__))
os.path.dirname(os.path.abspath("__file__"))
'''This script was the main script used to filter the data'''

def usage():
    some_advice=''' '''

def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)
        print(path +"\tis ok")
    else:
        print (path+"\thas been existed")


def read_software(software):
    '''获取软件列表，读取软件路径便于迁移'''
    global soft
    soft={}
    with open(software) as s:
        for line in s:
                tmps=line.strip().split("=")
                soft[tmps[0]]=tmps[1]
                #print(tmps[0],tmps[1])

def read_adapter(adapter):
    global adap
    adap={}
    pat1=re.compile("forward")
    pat2=re.compile("reverse")
    with open(adapter) as ad:
        for line in ad:
            line=line.strip()
            if line.startswith(">") and re.search(pat1,line):
                adap["p7"]=next(ad).rstrip()
            elif line.startswith(">") and re.search(pat2,line):
                adap["p5"]=next(ad).rstrip()
            else:
                raise Exception("adapter文件不是4行，或者不含有forward或reverse字样")
    print (adap["p7"])
    print (adap["p5"])

def make_adapter(sample,outdir):
    """输出每个read的adapter信息"""
    f=open(outdir+"/adapter.sh","a")
    pat1=re.compile('1\.fq\.gz$|1\.fastq\.gz$')
    pat2=re.compile('2\.fq\.gz$|2\.fastq\.gz$')
    output=str(sample)+".adapter"
    output_tmp=output+".tmp"
    if re.search(pat1,str(sample)):
        f.write("{0} -a {1} -O 5 --info-file={2} {3}>/dev/null 2>&1 && awk -F \"\\t\"'{{if ($2!=-1)print}}' {2}>{4} && gzip {4} && rm {2}\n".format(soft["cutadapt"],adap["p7"],output_tmp,sample,output))
    elif re.search(pat2,str(sample)):
        f.write("{0} -a {1} -O 5 --info-file={2} {3}>/dev/null 2>&1 && awk -F \"\\t\" '{{if ($2!=-1)print}}' {2}>{4} && gzip {4} && rm {2}\n".format(soft["cutadapt"],adap["p5"],output_tmp,sample,output))
    else:
        raise Exception(sample+"\t"+"存在问题")


def arrange_dir(indir,outdir):

    '''寻找数据目录中所有的后缀为fastq.gz和fq.gz的文件，将其链接到项目目录的rawdata文件夹'''
    sample_list=open(outdir+"/sample.list","w")
    read_adapter(bindir+"/../config/illumina_adapters.fa")
    read_software(bindir+"/../config/Software.txt")
    mkdir(outdir+"/Cleandata")
    mkdir(outdir+"/Rawdata")
    pat1=re.compile('fq\.gz$|fastq\.gz$')
    pat2=re.compile('(\S+?)_?R?\d?\.f\w+?\.gz$')
    for root,dirs,files in os.walk(indir,topdown=False):
        for name in files:
            if re.search(pat1,name):
                m=pat2.match(name)
                mkdir("{0}/Cleandata/{1}".format(outdir,m.group(1)))
                mkdir("{0}/Rawdata/{1}".format(outdir,m.group(1)))
                os.symlink(os.path.join(root,name),"{0}/Rawdata/{1}/{2}".format(outdir,m.group(1),name))
                sample_list.write("{1}\t{0}/Rawdata/{1}/{2}\t{0}/Cleandata/{1}/{2}\n".format(outdir,m.group(1),name))
                make_adapter("{0}/Rawdata/{1}/{2}".format(outdir,m.group(1),name),outdir)

def fq_filter(outdir):
    raw_R1={}
    raw_R2={}
    clean_R1={}
    clean_R2={}
    seq=[]
    pat1=re.compile('\S+?_?R?1\.f\w+?\.gz$')
    pat2=re.compile('\S+?_?R?2\.f\w+?\.gz$')
    with open(outdir+"/sample.list") as fff:
        for line in fff:
            tmps=line.strip().split("\t")
            seq.append(tmps[0])
            if re.search(pat2,tmps[1]):
                raw_R2[tmps[0]]=tmps[1]
                clean_R2[tmps[0]]=tmps[2]
            else:
                raw_R1[tmps[0]]=tmps[1]
                clean_R1[tmps[0]]=tmps[2]
    seq=list(set(seq))
    filter_sh=open(outdir+"/filter.sh","w")
    for i in seq:
        if i not in raw_R2:
            filter_sh.write("python3 {0}/FQ_QC.py -i1 {1} -o1 {2}\n".format(bindir,raw_R1[i],clean_R1[i]))
            filter_sh.write("perl {0}/stat_fq.pl {1} {2}\n".format(bindir,clean_R1[i],clean_R1[i]+".report"))
            filter_sh.write("python3 {0}/draw_base_quality_distribution_v1.py -r1 {1} -s {2}\n".format(bindir,clean_R1[i]+".report",i))
            filter_sh.write("perl {0}/stat_fq.pl {1} {2}\n".format(bindir,raw_R1[i],raw_R1[i]+".report"))
            filter_sh.write("python3 {0}/draw_base_quality_distribution_v1.py -r1 {1} -s {2}\n".format(bindir,raw_R1[i]+".report",i))
        else:
            filter_sh.write("python3 {0}/FQ_QC.py -i1 {1} -i2 {2} -o1 {3} -o2 {4}\n".format(bindir,raw_R1[i],raw_R2[i],clean_R1[i],clean_R2[i]))
            filter_sh.write("perl {0}/stat_fq.pl {1} {2}\n".format(bindir,clean_R1[i],clean_R1[i]+".report"))
            filter_sh.write("perl {0}/stat_fq.pl {1} {2}\n".format(bindir,clean_R2[i],clean_R2[i]+".report"))
            filter_sh.write("python3 {0}/draw_base_quality_distribution_v1.py -r1 {1} -r2 {2} -s {3}\n".format(bindir,clean_R1[i]+".report",clean_R2[i]+".report",os.path.dirname(clean_R2[i]+".report")+"/"+i))
            filter_sh.write("perl {0}/stat_fq.pl {1} {2}\n".format(bindir,raw_R1[i],raw_R1[i]+".report"))
            filter_sh.write("perl {0}/stat_fq.pl {1} {2}\n".format(bindir,raw_R2[i],raw_R2[i]+".report"))
            filter_sh.write("python3 {0}/draw_base_quality_distribution_v1.py -r1 {1} -r2 {2} -s {3}\n".format(bindir,raw_R1[i]+".report",raw_R2[i]+".report",os.path.dirname(raw_R2[i]+".report")+"/"+i))
        


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('-i','--indir',help='the input dir of the fastq',dest='indir',required=True)
    parser.add_argument('-o','--outdir',help='the outdir of clean fastq',dest='outdir',required=True)
    #parser.add_argument('-n','--n_rate',help="The rate of N",dest='n_rate',required=True,type=float)
    #parser.add_argument('-q','--quality',help="under the  phred score need be calulated",dest='quality',required=True,type=int)
    #parser.add_argument('-l','--low_rate',help="the max rate of low quality base in a read",dest="low_rate",required=True,type=float)
    
    args=parser.parse_args()
    args.indir=os.path.abspath(args.indir)
    mkdir(args.outdir)
    args.outdir=os.path.abspath(args.outdir)
    arrange_dir(args.indir,args.outdir)
    fq_filter(args.outdir)
if __name__=="__main__":
    main()
 #read_adapter(sys.argv[1])

