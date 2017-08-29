###################################################################
# File Name: table2html.py
# Author: yaomingyue
# mail: yaomingyue@fuanhua.com
# Created Time: 2017年08月29日 星期二 08时53分20秒
#=============================================================
#!/usr/bin/env python
#-*- coding:utf8 -*-
import sys
import smtplib
from email.mime.text import MIMEText
'''This script was used to convert the table to html and send an Email.'''
def sendemail(content,title,receivers):
    #设置服务器所需信息
    #163邮箱服务器地址
    mail_host = 'smtp.163.com'  
    #163用户名
    mail_user = 'FAH_ngs'  
    #密码 
    mail_pass = 'FAH888'   
    #邮件发送方邮箱地址
    sender = 'FAH_ngs@163.com'  
    #设置email信息
    #邮件内容设置
    message = MIMEText(content,'html','utf-8')
    #邮件主题       
    message['Subject'] = title 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  
    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
def table2html(table):
    with open(table) as f:
        tag=0
        html='''<table border="1">\n'''
        for line in f:
            tag+=1
            tmps=line.rstrip().split("\t")
            if tag==1:
                html+="<tr>\n"
                for i in tmps:
                    html+="<th>{0}</th>\n".format(i)
                html+="</tr>\n"
            else:
                html+="<tr>\n"
                for j in tmps:
                    html+="<td>{0}</td>\n".format(j)
                html+="<tr>\n"
    return html

if __name__=="__main__":
    abc=table2html(sys.argv[1])
    title="质量控制已完成，请查看"
    receivers=["yaomingyue@fuanhua.com"]
    sendemail(abc,title,receivers)
    
                
