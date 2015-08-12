#! /usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8
'''
关于接口的操作
'''
import httplib,urllib
import urllib2,json
import requests
import ssl,sys
import SendEmail
import StoreData
import ConfigParser
import time,commands
import sys,unicodedata
reload(sys)
sys.setdefaultencoding('utf8')

cf=ConfigParser.ConfigParser()
cf.read("email.conf")
#CONFIG
FILE_UPLOAD_URL=cf.get("HTTP","FILE_UPLOAD_URL")
REPUTATION_QUERY_URL=cf.get("HTTP","QUERY_URL")
SUBJECT=cf.get("EMAIL","SUBJECT")
CONTENT=cf.get("EMAIL","CONTENT")

ISOTIMEFORMAT='%Y-%m-%d %X'
#FUNCTIONS

def easyHttp(md5):
    '''
    查询

    '''
    url=QUERY_URL
    payload={'md5':md5}
    r=requests.get(url,params=payload)
    #print r.status_code
    #print r.headers
    #print r.json()
    return r.json()
def fileUploadHttp(filename,file_path,md5,email_address,email_uidl):
    '''
    上传文件（使用中）
    '''
    #reload(sys)
    #sys.setdefaultencoding("utf-8")
    #ssl._create_default_https_context = ssl._create_unverified_context
    reputation_result=easyHttp(md5)
    if reputation_result=='None':
        url=FILE_UPLOAD_URL
        #print file_path.__class__
        if not has_hz(unicode_parse(file_path)):
            path=u'%s'%file_path
            filename=urllib.quote(filename)
            files={'file':(filename,open(path,'rb'))}
            request = requests.Session()
            response=requests.post(url,files=files)
            #print response.status_code
            #print response.headers
            #result=eval(response.text)
            result=response.json()
            file_object=open(cf.get("EMAIL","OUTDIR")+"/remoteUpload.log",'a')
            file_object.write(response.text)
            file_object.write(time.strftime(ISOTIMEFORMAT, time.localtime())+"\n")
            file_object.close()
        else :
            return False

    else :
        return True
def reputationHttp():
    '''
    未使用
    '''
    ssl._create_default_https_context = ssl._create_unverified_context
    API_URL=REPUTATION_QUERY_URL
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'# 将user_agent写入头信息
    headers = {"Content-Type":"application/json",'User-Agent' : user_agent }
    try:
        request=urllib2.Request(API_URL,json.dumps([{"md5":"832f4c572afd6fab474e3a7a87299707"}]),headers)
        print(request)
        response=urllib2.urlopen(request)
        #print response.status
        #print response.reason
        print response.read()
        print response.getheaders()
    except Exception,e:
        print e
def queryHttp(md5):
    '''
    未使用
    '''
    #reload(sys)
    #sys.setdefaultencoding("utf-8")
    #ssl._create_default_https_context = ssl._create_unverified_context
    url=REPUTATION_QUERY_URL
    print url
    payload={'md5':'f760e7552230a88cb16d8132eee80d49'}
    headers={'content-type':'application/json'}
    r=requests.post(url,data=json.dumps(payload),headers=headers)
    #r=requests.post(url,verify=False)
    print r.status_code
    print r.headers
    print r.text
    #print r.content
    #print r.text

def originHttp():
    '''
    未使用
    '''
    httpClient=None
    try:
    	params=urllib.urlencode({'md5':'832f4c572afd6fab474e3a7a87299707'})
    	headers={"Content-type":"application/x-www-form-urlencoded","Accept":"text/plain"}
    	httpClient=httplib.HTTPConnection("10.6.109.103",8000,timeout=30)
    	httpClient.request("POST","/apps/samplesamplerecord/search",params,headers)
    	response=httpClient.getresponse()
    	print response.status
    	print response.reason
    	print response.read()
    	print response.getheaders()
    except Exception,e:
    	print e
    finally:
    	if httpClient:
    		httpClient.close()
def parse_str(string):
    if isinstance(string,int):
        return str(string)
    elif string==None:
        return "空"
    else :
        return string.decode('ascii').encode('utf-8')
def has_hz(text):
    hz_yes = False
    for ch in text:
        if isinstance(ch, unicode):
            if unicodedata.east_asian_width(ch)!= 'Na':
                hz_yes = True
                break
        else:
            continue   
       
    return hz_yes    
def unicode_parse(text):
    if isinstance(text,unicode):
        return text
    else:
        return text.decode('gb2312')

if __name__ == '__main__':
    #originHttp()
    #reputationHttp()
    #queryHttp("f760e7552230a88cb16d8132eee80d49")

    url=FILE_UPLOAD_URL
    path="E:\\fakename_3999.exe"
    filename=urllib.quote("fakename_3999.exe")
    files={'file':open(path,'rb')}
    print files
    response=requests.post(url,files=files)
    print response
    print response.json()