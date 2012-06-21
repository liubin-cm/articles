'''
Created on 2012-03-09

@author: binliu
'''
import os
import sys
import subprocess

class pyruncmd(object):
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
                self.out = str(self.out,'gb2312','ignore')
                self.err = str(self.err,'gb2312','ignore')
            else:
                self.out = str(self.out,'utf-8')
                self.err = str(self.err,'utf-8')
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
                return_lines.append(line.strip())
        return(return_lines)

    #max_returncode为命令执行正常时的最大返回值，如果超过此最大返回值，则引发pycmd_run_error异常
    #通常情况下max_remax_returncode为0
    def is_cmd_succeeded(self, max_returncode = 0):
        if self.run() and 0 <= self.get_returncode() <= max_returncode:
            print(self.command_str.split("password")[0] + " normal.")
            print(self.get_stdout_all())
        else:
            print(self.command_str.split("password")[0] + " run error!")
            print(self.get_stdout_all())
            print(self.get_stderr())
            print("退出码：" + str(self.get_returncode()))
            raise Exception(self.command_str.split("password")[0] + " run error!")
        
if __name__ == "__main__":
    cmd = pyruncmd()
    cmd.command_str = "dir"
    print(cmd.run())
    print(cmd.get_returncode())
    print(cmd.get_stdout_all())
    print(cmd.get_stdout_lines())
    try:
        cmd.is_cmd_succeeded(0)
    except Exception as e:
        print(e.value)