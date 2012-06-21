'''
Created on 2012-3-12

@author: binliu
'''

import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.base import MIMEBase 
from email.mime.text import MIMEText 
from email import utils
from email import encoders
from email.header import Header
import os 
import sys

class pyemail(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    @staticmethod
    def send(to, subject, content, attachments=[],server="mail.5173.com"): 
        '''
                    发送邮件的静态方法,其中to以逗号分割
        '''
        if sys.platform.find("win") > -1:
            charset = 'gb2312'
        else:
            charset = 'utf-8'

        fro = "autopost <autopost@5173.com>" 
     
        msg = MIMEMultipart() 
        msg['From'] = fro 
        msg['To'] = to
        msg['Date'] = utils.formatdate(localtime=True) 
        msg['Subject'] = Header(subject, "utf-8")
        
        if content == "":
            content = " "
        msg.attach(MIMEText(content,"plain","utf-8")) 

        for file in attachments: 
            #file = str(file, 'gb2312')
            part = MIMEBase('application', "octet-stream") 
            part.set_payload( open(file,"rb").read() ) 
            encoders.encode_base64(part) 


            part.add_header('Content-Disposition', 'attachment; filename="%s"' 
                           %  str(os.path.basename(file).encode(charset), charset))
            msg.attach(part) 
     
        smtp = smtplib.SMTP(server) 
        smtp.login('autopost@5173.com',"84u31tiyW3A27qk")
        smtp.sendmail(fro, [i.strip() for i in to.split(',')], msg.as_string()) 
        smtp.close()

if __name__ == '__main__':  
    pyemail.send("liubin,scm", "nihao", "")