###################################################################
# File Name: read_datasets_basecaller_json.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年11月13日 星期一 15时14分15秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
'''This script was used to read the datasets_basecaller.json'''
import json
import sys

NOTE='''Usage:\n\tpython3 {0} <input_json>\n'''.format(sys.argv[0])

def read_json(json_input):
	dic={}
	ff=open(json_input,encoding='utf-8')
	setting=json.load(ff)
	for i in setting["read_groups"]:
		if "barcode_name" not in setting["read_groups"][i]:
			dic["nomatch"]=setting["read_groups"][i]["read_count"]
		else:
			dic[setting["read_groups"][i]["barcode_name"]]=setting["read_groups"][i]["read_count"]
	return dic

def main():
	dic=read_json(sys.argv[1])
	for i in sorted(dic.keys()):
		print(i,dic[i])

if __name__=="__main__":
	if len(sys.argv)!=2:
		print(NOTE)
		exit(0)
	main()
