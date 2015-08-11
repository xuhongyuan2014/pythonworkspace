#! /usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8
import sys,os
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf8')

cf=ConfigParser.ConfigParser()
cf.read("email.conf")
#CONFIG

import struct 
#允许的文件类型
ALLOW_TYPE_LIST=["RAR","ZIP"] 
# 支持文件类型  
# 用16进制字符串的目的是可以知道文件头是多少字节  
# 各种文件头的长度不一样，少半2字符，长则8字符  
def typeList():  
    return {  
        "52617221":"RAR",  
        "504B0304":"ZIP",
        "FFD8FF":"JPEG",
        "89504E47":"PNG",
        "68746D6C3E":"HTML",
        "3C3F786D6C":"XML",
        "D0CF11E0":"MS Word/Excel"}    
# 字节码转16进制字符串  
def bytes2hex(bytes):  
    num = len(bytes)  
    hexstr = u""  
    for i in range(num):  
        t = u"%x" % bytes[i]  
        if len(t) % 2:  
            hexstr += u"0"  
        hexstr += t  
    return hexstr.upper()  
  
# 获取文件类型  
def filetype(filename):  
    binfile = open(filename, 'rb') # 必需二制字读取  
    tl = typeList()  
    ftype = 'unknown'  
    for hcode in tl.keys():  
        numOfBytes = len(hcode) / 2 # 需要读多少字节  
        binfile.seek(0) # 每次读取都要回到文件头，不然会一直往后读取  
        hbytes = struct.unpack_from("B"*numOfBytes, binfile.read(numOfBytes)) # 一个 "B"表示一个字节  
        f_hcode = bytes2hex(hbytes)  
        if f_hcode == hcode:  
            ftype = tl[hcode]  
            break  
    binfile.close()  
    return ftype  
def validAttachment(filename,file_path,email_address):
    file_type=filetype(file_path)
    result={}
    if file_type in ALLOW_TYPE_LIST:
        if file_type=="ZIP":
            pass
        if file_type=="RAR":
            pass
    else :
        pass
    return result
def unicode_parse(text):
    if isinstance(text,unicode):
        return text
    else:
        return text.decode('gb2312')
if __name__ == '__main__':  
    print validAttachment("","/home/test.rar","")
