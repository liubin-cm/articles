'''
Created on 2011-11-27

@author: binliu
'''

import os
import sys
import subprocess

class pywincmd(object):
    '''
    封装操作系统命令的对象
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.command_str = ""
        
    def run(self):
        try:
            self.p = subprocess.Popen(self.command_str, shell=True, stderr = subprocess.PIPE, stdout = subprocess.PIPE)
            (self.out, self.err) = self.p.communicate()
            if sys.platform.find("win") > -1:
                self.out = str(self.out,'gb2312')
                self.err = str(self.err,'gb2312')
            else:
                self.out = str(self.out,'utf-8')
                self.err = str(self.err,'utf-8')
            #raise OSError('span','ok')
        except (OSError, ValueError) as e:
            print(self.command_str.split("password")[0] + " makes a error:",e)
            return(False)
        else:
            return(True)
            
    def get_returncode(self):
        return(self.p.wait())
        
    def get_stdout_all(self):
        return(self.out)
        
    def get_stderr(self):
        return(self.err)
    
    def get_stdout_lines(self):
        lines = self.out.split(os.linesep)
        return_lines = []
        for line in lines:
            if line.strip() == "":
                pass
            else:
                return_lines.append(line)
        return(return_lines)

    def is_cmd_succeeded(self):
        if self.run() and self.get_returncode() == 0:
            print(self.command_str.split("password")[0] + " normal.")
            print(self.get_stdout_all())
        else:
            print(self.command_str.split("password")[0] + " run error!")
            print(self.get_stdout_all())
            print(self.get_stderr())
            exit(1)

class pysvn(object):
    '''
    常用的svn操作
    '''
    py_cmd = pywincmd()

    def __init__(self):
        '''
        Constructor
        '''
           
    @staticmethod
    def co(url, revision, path, username, password):
        pysvn.py_cmd.command_str = "echo p|svn co \"" + url + r"@" + revision + "\" \"" + path + "\" " + " --username " + username + " --password " + password #+ " --trust-server-cert " + "--non-interactive"
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_all())
    
    @staticmethod
    def up(revision, path, username, password):
        pysvn.py_cmd.command_str = "echo p|svn up -r " + revision + " \"" + path + "\" " + " --username " + username + " --password " + password #+ " --trust-server-cert " + "--non-interactive"
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_all())

if __name__ == '__main__':  
    workspace = os.getenv("WORKSPACE")
    path = workspace + os.sep + "sbp_2.0"
    if os.path.exists(path):
        pysvn.up("HEAD", path, "301645", "//5173@#q")
    else:
        pysvn.co("https://192.168.140.28/svn_product/sbp/sbp_2.0", "HEAD", path, "301645", "//5173@#q")
