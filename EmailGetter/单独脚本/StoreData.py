# -*- coding: utf-8 -*-
#encoding=utf-8
import MySQLdb

def insert_attachment(file_name,md5,email_uidl,email_address,date):
	'''
	插入附件信息到MySQL数据库

	参数：文件名，MD5，邮件UIDL，邮件地址from，邮件日期
	'''
	try:
		conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',port=3306,charset='gbk')
		cur=conn.cursor()
		sql_content="insert into attachment(file_name,md5,email_uidl,email_address,date) values ('%s','%s','%s','%s','%s')" %(file_name,md5,email_uidl,email_address,date)
                #print(file_name)
		cur.execute(sql_content)
		print("    Insert Attachment Success!"+sql_content)
		cur.close()
		conn.commit()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" %(e.args[0],e.args[1])

def insert_email_info(email_uidl,email_address,date):
	'''
	插入邮件信息到数据库

	参数：邮件uidl,邮件地址，邮件时间
	'''
	try:
		conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',port=3306)
		cur=conn.cursor()
		sql_content="insert into email(email_uidl,email_address,date) values ('%s','%s','%s')" %(email_uidl,email_address,date)
		result=cur.execute(sql_content)
		print("    Insert Email Success!"+sql_content)
		cur.close()
		conn.commit()
		conn.close()
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" %(e.args[0],e.args[1])

def is_email_unread(email_uidl):
	'''
	根据邮件uidl判断邮件是否未读

	参数：邮件uidl
	返回值：True：未读;False:已读
	'''
	try:
		conn=MySQLdb.connect(host='localhost',user='root',passwd='root',db='test',port=3306)
		cur=conn.cursor()
		sql_content="select 1 from email where email_uidl = '%s' limit 1" %(email_uidl)
		result=cur.execute(sql_content)
		print("    Select Email_UIDL Success!"+sql_content)
		cur.close()
		conn.commit()
		conn.close()
		if result==1:
			return False
		else:
			return True
	except MySQLdb.Error,e:
		print "Mysql Error %d: %s" %(e.args[0],e.args[1])