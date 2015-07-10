#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
获取邮件的方法类

使用示例：
import GetEmailXX as g
if __name__ == "__main__":
  getter=g.EmailGetter()
  print(getter.start())
返回值：[获取的未读邮件数量，获取的新附件数量]
[result_unread_num,result_file_num]
'''
import os
import re
import time
import email
import poplib
import imaplib
import cStringIO
import StoreData
from hashlib import md5
import md5

class EmailGetter(object):

    # Configuration
    # -------------

    # Email address
    MAILADDR = ""

    # Email password
    PASSWORD = ""

    # Mail Server (pop/imap)
    SERVER = ""

    # Transfer protocol (pop3/imap4)
    PROTOCOL = "pop3"

    # Use SSL? (True/False)
    USE_SSL = True

    # Main output direcotory
    OUTDIR = "result"


    # Variables
    result_file_num=0
    result_unread_num=0
    result_path=""
    result_file=""
    # Static variable
    # ---------------

    # Default port of each protocol
    DEFAULT_PORT = {
        "pop3": {False: 110, True: 995},
        "imap4": {False: 143, True: 993},
    }

    def __init__(self,MAILADDR = "",PASSWORD = "",SERVER = ""):
        self.MAILADDR=MAILADDR
        self.PASSWORD=PASSWORD
        self.SERVER=SERVER
        
    def set_outdir(self,outdir):
        self.OUTDIR=outdir

    def set_protocol(self,protocol):
        self.PROTOCOL=protocol

    # Function
    # --------

    def exit_script(self,reason, e=""):
        """Print error reason and exit this script
        
        :param reason: exit error reason
        :param e: exception
        """
        # Print exit string
        exit_str = "[-] {0}".format(reason)
        if e:
            exit_str += " ({0})".format(e)
        print(exit_str)
        
        # Remove result path
        self.remove_dir(self.result_path)
        
        # Exit script
        print("[-] Fetch email failed!")
        exit(-1)

    def parse_protocol(self,protocol):
        """Parse transfer protocol
        
        :param protocol: transfer protocol
        :return: handled protocol
        """
        if protocol in ["pop", "pop3"]:
            return "pop3"
        elif protocol in ["imap", "imap4"]:
            return "imap4"
        else:
            self.exit_script("Parse protocol failed: {0}".format(protocol))

    def parse_server(self,server, use_ssl, protocol):
        """Change server to host and port. If no port specified, use default value
        
        :param server: mail server (host, host:port)
        :param use_ssl: True if use SSL else False
        :param protocol: transfer protocol (pop3/imap4)
        :return: host and port
        """
        if not server:
            self.exit_script("No available server")
        
        server_item = server.split(":")
        server_item_len = len(server_item)
        
        if server_item_len > 2:
            exit_script("Too many colons in server: {0}".format(server))
        
        try:
            host = server_item[0]
            port = self.DEFAULT_PORT[protocol][use_ssl] if server_item_len == 1 else int(server_item[1])
        except BaseException as e:
            self.exit_script("Parse server format failed: {0}".format(server), e)
        return host, port

    def create_dir(self,result_path):
        """Create output directory if not exist
        
        :param result_path: main result path
        """
        try:
            if not os.path.exists(result_path):
                os.mkdir(result_path)
                print("[*] Create directory {0} successfully".format(result_path))
            else:
                if os.path.isfile(result_path):
                    self.exit_script("{0} is file".format(result_path))
                else:
                    print("[*] Directory {0} has already existed".format(result_path))
        except BaseException as e:
            self.exit_script("Create directory {0} failed".format(result_path), e)

    def remove_dir(self,result_path):
        """Remove output directory if no file in this directory
        
        :param result_path: main result path
        """
        try:
            if os.path.isdir(result_path):

                if len(os.listdir(result_path)) == 0:
                    os.rmdir(result_path)
                    print("[*] Remove directory {0} successfully".format(result_path))
                else:
                    print("[*] Directory {0} is not empty, no need remove".format(result_path))
            else:
                print("[*] No directory {0}".format(result_path))
        except BaseException as e:
            print("[-] Remove directory {0} failed: {1}".format(result_path, e))

    def protocol_manager(self,protocol, host, port, usr, pwd, use_ssl):
        """Choose handle function according to transfer protocol
        
        :param protocol: transfer protocol (pop3/imap4)
        :param host: host
        :param port: port
        :param usr: username
        :param pwd: password
        :param use_ssl: True if use ssl else False
        """
        #atObj=EmailGetter()

        '''
        import __main__
        if hasattr(__main__, protocol):
            getattr(__main__, protocol)(host, port, usr, pwd, use_ssl)
        else:
            exit_script("Wrong protocol: {0}".format(protocol))
            '''
        if hasattr(self, protocol):
            getattr(self, protocol)(host, port, usr, pwd, use_ssl)
        else:
            self.exit_script("Wrong protocol: {0}".format(protocol))

    def pop3(self,host, port, usr, pwd, use_ssl):
        """Pop3 handler
        
        :param host: host
        :param port: port
        :param usr: username
        :param pwd: password
        :param use_ssl: True if use SSL else False
        """
        # Connect to mail server
        try:
            conn = poplib.POP3_SSL(host, port) if use_ssl else poplib.POP3(host, port)
            conn.user(usr)
            conn.pass_(pwd)
            print("[+] Connect to {0}:{1} successfully".format(host, port))
        except BaseException as e:
            self.exit_script("Connect to {0}:{1} failed".format(host, port), e)
        
        # Get email message number
        try:
            msg_num = len(conn.list()[1])
            print("[*] {0} emails found in {1}".format(msg_num, usr))
        except BaseException as e:
            self.exit_script("Can't get email number", e)  
        # Get email content and attachments
        #for i in range(1, msg_num+1):
        for current_email_des in conn.uidl()[1]:
            current_msg_num=current_email_des.split(" ")[0]
            current_email_uidl=current_email_des.split(" ")[1]
            #print(current_email_uidl)
            #print(StoreData.is_email_unread(current_email_uidl))
            if StoreData.is_email_unread(current_email_uidl):#如果该邮件未读，则进行下载并解析
                print("[*] Unread Eamil ! Downloading email {0}/{1}---uidl:{2}".format(current_msg_num, msg_num,current_email_uidl))
                #if i==11: conn.dele(i)#删除邮件
                # Retrieve email message lines, and write to buffer
                try:
                    msg_lines = conn.retr(current_msg_num)[1]
                    
                    buf = cStringIO.StringIO()
                    for line in msg_lines:
                        print >> buf, line
                    buf.seek(0)
                except BaseException as e:
                    print "[-] Retrieve email {0} failed: {1}".format(current_msg_num, e)
                    continue
                
                # Read buffer
                try:
                    msg = email.message_from_file(buf)
                except BaseException as e:
                    print "[-] Read buffer of email {0} failed: {1}".format(current_msg_num, e)
                    continue
                
                # Parse and save email content/attachments
                try:
                    #print("    "+get_date(msg)+"|From :"+get_from(msg)+"|To:"+get_to(msg))
                    self.parse_email(msg, current_msg_num,current_email_uidl)
                except BaseException as e:
                    print("[-] Parse email {0} failed: {1}".format(current_msg_num, e))
            else:
                print("[*] Read Email ! Cancel Downloading email {0}/{1}---uidl:{2}".format(current_msg_num, msg_num,current_email_uidl))
        # Quit mail server
        conn.quit()
        
    def imap4(self,host, port, usr, pwd, use_ssl):
        """Imap4 handler
        
        :param host: host
        :param port: port
        :param usr: username
        :param pwd: password
        :param use_ssl: True if use SSL else False
        """
        # Connect to mail server
        try:
            conn = imaplib.IMAP4_SSL(host, port) if use_ssl else imaplib.IMAP4(host, port)
            conn.login(usr, pwd)
            print(conn.status('INBOX','(MESSAGES RECENT UIDNEXT UIDVALIDITY UNSEEN)'))
            print("[+] Connect to {0}:{1} successfully".format(host, port))
        except BaseException as e:
            self.exit_script("Connect to {0}:{1} failed".format(host, port), e)
        
        # Initial some variable
        list_pattern = re.compile(r'\((?P<flags>.*?)\) "(?P<delimiter>.*)" (?P<name>.*)')
        download_num = 0
        download_hash = []
        
        # Get all folders
        try:
            type_, folders = conn.list()
        except BaseException as e:
            self.exit_script("Get folder list failed", e)
        
        for folder in folders:
            # Parse folder info and get folder name
            try:
                flags, delimiter, folder_name = list_pattern.match(folder).groups()
                folder_name = folder_name.strip('"')
                print "[*] Handling folder: {0}".format(folder_name)
            except BaseException as e:
                print "[-] Parse folder {0} failed: {1}".format(folder, e)
                continue
            
            # Select and search folder
            try:
                conn.select(folder_name, readonly=True)
                type_, data = conn.search(None, "ALL")
            except BaseException as e:
                print "[-] Search folder {0} failed: {1}".format(folder_name, e)
                continue
            
            # Get email number of this folder
            try:
                msg_id_list = [int(i) for i in data[0].split()]
                msg_num = len(msg_id_list)
                print "[*] {0} emails found in {1} ({2})".format(msg_num, usr, folder_name)
            except BaseException as e:
                print "[-] Can't get email number of {0}: {1}".format(folder_name, e)
                continue
            
            # Get email content and attachments
            for i in msg_id_list:
                print "[*] Downloading email {0}/{1}".format(i, msg_num)
                
                # Get email message
                try:
                    type_, data = conn.fetch(i, "(RFC822)")
                    msg = email.message_from_string(data[0][1])
                except BaseException as e:
                    print "[-] Retrieve email {0} failed: {1}".format(i, e)
                    continue
                
                # If message already exist, skip this message
                try:
                    msg_md5 = md5(data[0][1]).hexdigest()
                    if msg_md5 in download_hash:
                        print "[-] This email has been downloaded in other folder"
                        continue
                    else:
                        download_hash.append(msg_md5)
                        download_num += 1
                except BaseException as e:
                    print "[-] Parse message md5 failed: {0}".format(e)
                    continue
                
                # Parse and save email content/attachments
                try:
                    self.parse_email(msg, download_num,email_uidl)#此处email_uidl暂时未定义
                except BaseException as e:
                    print "[-] Parse email {0} failed: {1}".format(i, e)
        
        # Logout this account
        conn.logout()
            
    def parse_email(self,msg, i,email_uidl):
        """Parse email message and save content & attachments to file
        
        :param msg: mail message
        :param i: ordinal number
        """
        #global result_file
        email_date=self.get_date(msg)
        email_address_store=self.get_from(msg)
        if email_date!=None:
            date_store="%s-%s-%s %s:%s"%(email_date[0],email_date[1],email_date[2],email_date[3],email_date[4])
        else:
            date_store="%s-%s-%s %s:%s"%(0,0,0,0,0)
        StoreData.insert_email_info(email_uidl,email_address_store,date_store)
        self.result_unread_num=self.result_unread_num+1
        # Parse and save email content and attachments
        for part in msg.walk():
            if not part.is_multipart():
                filename = part.get_filename()
                #content = part.get_payload(decode=True)
                charset = self.get_charset(part)
                
                if charset == None: #modified by mrxu
                    content = part.get_payload(decode=True)
                else:
                    content = part.get_payload(decode=True).decode(charset)
                    

                if filename:  # Attachment
                    # Decode filename
                    h = email.Header.Header(filename)
                    dh = email.Header.decode_header(h)
                    filename = dh[0][0]

                    filename_store="mail{0}_attach_{1}".format(i, filename)
                    #date_store="%s-%s-%s %s:%s"%(get_date(msg)[0],get_date(msg)[1],get_date(msg)[2],get_date(msg)[3],get_date(msg)[4])

                    self.result_file = os.path.join(self.result_path, "mail{0}_attach_{1}".format(i, filename))
                    #print(date_store)       
                    #print("now"+self.result_path)

                    print("[-] Found attachment:"+filename),
                    if self.is_file_exists("mail{0}_attach_{1}".format(i, filename)):
                        print("This File Exists")
                    else:
                        print("New File")
                        try:#输出文件(附件)
                            with open(self.result_file, "wb") as f:
                                f.write(content)
                        except BaseException as e:
                            print("[-] Write file of email {0} failed: {1}".format(i, e))
                        md5_store=self.GetFileMD5(self.result_file)
                        StoreData.insert_attachment(filename_store,md5_store,email_uidl,email_address_store,date_store)
                        self.result_file_num=self.result_file_num+1

                        
                else:  # Main content   modified by mrxu
                    print("    ContentType:"+self.get_content_type(part))
                    content_suffix=self.get_suffix(self.get_content_type(part))
                    self.result_file = os.path.join(self.result_path, "mail{0}_text".format(i)+content_suffix)           
                    '''
                    try:#输出文件(正文)
                        with open(result_file, "wb") as f:
                            f.write(content)
                    except BaseException as e:
                        print("[-] Write file of email {0} failed: {1}".format(i, e))
                        '''


    #获取发件人邮箱   added by mrxu 
    def get_from(self,msg):
        if msg != None:
            return email.utils.parseaddr(msg.get("from"))[1]
        else:
            empty_obj()

    #获取邮件的文本类型 added by mrxu
    def get_content_type(self,msg):
        if msg != None:
            return email.utils.parseaddr(msg.get('content-type'))[1]
        else:
            empty_obj()

    #获取正文内容后缀 added by mrxu
    def get_suffix(self,contenttype):
        if contenttype in ['text/plain']:
            return '.txt'
        if contenttype in ['text/html']:
            return '.htm'
        return ''

    #获取收件人邮箱 added by mrxu
    def get_to(self,msg):
        if msg != None:
            return email.utils.parseaddr(msg.get('to'))[1]
        else:
            empty_obj()
     
     
    #获取邮件的生成时间 added by mrxu
    def get_date(self,msg):
        if msg != None:
            return email.utils.parsedate(msg.get('date'))
            #return email.utils.parseaddr(msg.get('date'))[1]
        else:
            empty_obj()

    #判断路径下是否有该文件存在 added by mrxu
    def is_file_exists(self,file_name):
        if os.path.exists(os.path.join(self.result_path,file_name)):
            return True
        else:
            return False

    #获得字符编码方法 added by mrxu
    def get_charset(self,message, default="utf-8"):
        #Get the message charset
        return message.get_charset()
        return default

    #get md5 of a input file  added by mrxu
    def GetFileMD5(self,file):  
        fileinfo = os.stat(file)  
        if int(fileinfo.st_size)/(1024*1024)>1000:  
            return self.GetBigFileMD5(file)  
        m = md5.new()  
        f = open(file,'rb')  
        m.update(f.read())  
        f.close()  
        return m.hexdigest()  
      
      
    #get md5 of a input bigfile  added by mrxu
    def GetBigFileMD5(self,file):  
        m = md5.new()  
        f = open(file,'rb')  
        maxbuf = 8192  
      
      
        while 1:  
            buf = f.read(maxbuf)  
            if not buf:  
                break  
            m.update(buf)  
      
      
        f.close()  
        return m.hexdigest()  

    def start(self):
        print("[*] Start download email script")
        start_time = time.time()
        
        mailaddr = self.MAILADDR
        password = self.PASSWORD
        server = self.SERVER
        protocol = self.PROTOCOL
        use_ssl = self.USE_SSL
        outdir = self.OUTDIR
        self.result_path = os.path.join(outdir, mailaddr)
        protocol = self.parse_protocol(protocol)
        host, port = self.parse_server(server, use_ssl, protocol)
        self.create_dir(self.result_path)
        #print(self.result_path)
        self.protocol_manager(protocol, host, port, mailaddr, password, use_ssl)
        self.remove_dir(self.result_path)
        #print(self.result_path)
        end_time = time.time()
        exec_time = end_time - start_time
        print("[*] Finish download email of {0} in {1:.2f}s".format(mailaddr, exec_time))
        return [self.result_unread_num,self.result_file_num]
