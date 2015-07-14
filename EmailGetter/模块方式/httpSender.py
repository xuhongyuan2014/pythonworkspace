#! /usr/bin/env python
# -*- coding: utf-8 -*-
#encoding=utf-8
import httplib,urllib
import urllib2,json
import requests
import ssl,sys
def reputationHttp():
    '''
    查询文件信誉

    '''
    ssl._create_default_https_context = ssl._create_unverified_context
    API_URL="https://10.6.109.10/file/search/f760e7552230a88cb16d8132eee80d49"
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'# 将user_agent写入头信息
    headers = {"Content-Type":"application/json",'User-Agent' : user_agent }
    try:
        request=urllib2.Request(API_URL,json.dumps([{"md5":"f760e7552230a88cb16d8132eee80d49"}]),headers)
        print(request)
        response=urllib2.urlopen(request)
        print("1")
        #print response.status
        #print response.reason
        print response.read()
        print response.getheaders()
    except Exception,e:
        print e
def queryHttp(md5):
    #reload(sys)
    #sys.setdefaultencoding("utf-8")
    ssl._create_default_https_context = ssl._create_unverified_context
    url="https://10.6.109.10/file/search/f760e7552230a88cb16d8132eee80d49"
    print url
    payload={'md5':'f760e7552230a88cb16d8132eee80d49'}
    headers={'content-type':'application/json'}
    cookies = dict(csrftoken='lJ7WnxQgGvFvcsngCOwdY1ylHL6R9QaM')
    r=requests.post(url,data=json.dumps(payload),headers=headers,verify=False,cookies=cookies)
    #r=requests.post(url,verify=False)
    print r.status_code
    print r.headers
    print r
    #print r.content
    #print r.text
def easyHttp(md5):
    url='https://10.6.109.10/file/search/'+md5
    cookies = dict(csrftoken='lJ7WnxQgGvFvcsngCOwdY1ylHL6R9QaM')
    print cookies
    r=requests.get(url,cookies=cookies,verify=False)
    print r.status_code
    print r.headers
def originHttp():
    httpClient=None
    try:
    	params=urllib.urlencode({'name':'mrxu','age':23})
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
def fileUploadHttp(file_path,md5):
    #reload(sys)
    #sys.setdefaultencoding("utf-8")
    ssl._create_default_https_context = ssl._create_unverified_context
    url='https://10.6.109.10/file/upload/'
    path='E:\mail9_attach_Desert.jpg'
    print(path)
    files={'file':open(path,'rb')}
    print(files)
    request = requests.Session()
    response=requests.post(url,files=files,verify=False)
    print response.status_code
    print response.headers
    print response.text
if __name__ == '__main__':
	#originHttp()
	#reputationHttp()
    queryHttp("f760e7552230a88cb16d8132eee80d49")
    easyHttp("f760e7552230a88cb16d8132eee80d49")
    #fileUploadHttp("E:\mail9_attach_Desert.jpg","")
