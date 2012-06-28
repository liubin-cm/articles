'''
Created on 2012-3-9

@author: 301645
'''

import sys
import os
from common.pyruncmd import pyruncmd
import re

class pysvn(object):
    py_cmd = pyruncmd()

    def __init__(self):
        '''
        Constructor
        '''
        
    @staticmethod
    def st(path):
        pysvn.py_cmd.command_str = 'svn st "' + path + '"'
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_lines())
    
    @staticmethod
    def co(url, path, username, password, revision = "HEAD", depth = "infinity"):
        pysvn.py_cmd.command_str = "echo p|svn co \"" + url + r"@" + revision + "\" \"" + path + "\" --depth " + depth + " --username " + username + " --password " + password
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_all())

    @staticmethod
    def up(path, username, password, revision = "HEAD"):
        pysvn.py_cmd.command_str = "echo p|svn up -r " + revision + " \"" + path + "\" " + " --username " + username + " --password " + password
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_all())

    @staticmethod
    def switch(url, revision, path, username, password):
        pysvn.py_cmd.command_str = "svn switch \"" + url + r'@' + revision + "\" \"" + path + "\" " + " --username " + username + " --password " + password + " --trust-server-cert " + "--non-interactive"
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_all())
    
    @staticmethod
    def info(path, username, password):
        pysvn.py_cmd.command_str = "echo p|svn info \"" + path + "\" --username " + username + " --password " + password
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_all())
    
    @staticmethod
    def log(url, username, password, revision = "HEAD", limit="1", quite = ""):
        '''
                    获取用户填写的日志信息
        '''
        if revision == "HEAD":
            pysvn.py_cmd.command_str = "echo p|svn log -l " + limit + " \"" + url + "\" " + quite + " --username " + username + " --password " + password
        else:
            pysvn.py_cmd.command_str = "echo p|svn log -l " + limit +  " -r " + revision + " \"" + url + "\" --username " + username + " --password " + password
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_all())
    
    @staticmethod
    def list(url, username, password, depth = "immediates"):
        pysvn.py_cmd.command_str = "echo p|svn list \"" + url + "\" --depth " + depth +  " --username " + username + " --password " + password
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_lines())
    
    @staticmethod
    def delete(path):
        pysvn.py_cmd.command_str = "svn del --force " + path
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_lines())
    
    @staticmethod
    def diff(path):
        pysvn.py_cmd.command_str = "svn diff " + path
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_lines())
    
    @staticmethod
    def merge(revision, url, username, password):
        pysvn.py_cmd.command_str = "svn merge -r HEAD:" + revision +" \"" + url + "\" --username " + username + " --password " + password + " --trust-server-cert " + "--non-interactive"
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_lines())
    
    @staticmethod
    def get_svn_diff_summarize(command, url,username, password):
        pysvn.py_cmd.command_str = command + " \"" + url + "\" --username " + username + " --password " + password + " --trust-server-cert " + "--non-interactive"
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_lines())
    
    @staticmethod
    def py_get_svn_info_revision(path, username, password):
        '''
                    获取svn info中的版本号
        '''
        info_out = pysvn.info(path, username, password)
        compile_pattern = re.compile("Revision:\s+\d+", re.I)
        all_matches = re.findall(compile_pattern, info_out)
        return(all_matches[0].split(":")[1].strip())
    
    @staticmethod
    def py_get_log_message(url, username, password, revision = "HEAD", limit="1", quite = ""):
        svn_log = pysvn.log(url, username, password, revision, limit, quite)
        lines = svn_log.split("\n")
        length = len(lines)
        if length >= 4:
            new_lines = lines[2:length-2]
            for i in range(0, len(new_lines)):
                new_lines[i] = new_lines[i].strip()
            return('\n'.join(new_lines))
        else:
            return('')
        
    @staticmethod
    def py_get_svn_info_url(path, username, password):
        '''
                    获取svn info中的url
        '''
        info_out = pysvn.info(path, username, password)
        compile_pattern = re.compile("URL:\s+\S+", re.I)
        all_matches = re.findall(compile_pattern, info_out)
        return(all_matches[0].split(":", 1)[1].strip())
                
    @staticmethod
    def clear_workingcopy(path):
        lines = pysvn.st(path)
        for line in lines:
            varpath = line.strip().split('    ')[-1].strip()
            if line.find('?') == 0 or line.find('A') == 0 :
                if line.find('A') == 0 :
                    pysvn.py_cmd.command_str = 'svn revert "' + varpath + '"'
                    pysvn.py_cmd.is_cmd_succeeded()
                if sys.platform.find("linux") > -1:
                    pysvn.py_cmd.command_str = 'rm -rf "' + varpath + '"'
                elif sys.platform.find("win") > -1:
                    if os.path.isfile(varpath):
                        pysvn.py_cmd.command_str = 'del /F /Q "' + varpath + '"'
                    else:
                        pysvn.py_cmd.command_str = 'rmdir /S /Q "' + varpath + '"'
                else:
                    pysvn.py_cmd.command_str = ""
            elif len(line) > 0:
                pysvn.py_cmd.command_str = 'svn revert "' + varpath + '"'
            else:
                pysvn.py_cmd.command_str = ""
            pysvn.py_cmd.is_cmd_succeeded()
    
    @staticmethod
    def clear_workingcopy_by_targets(path, targets):
        '''
        path为工作副本路径，targets为需要回滚的路径列表文件，路径列表是相对path的路径
        '''
        os.chdir(path)
        f = open(targets, 'r')
        lines = f.readlines()
        f.close()
        for line in lines:
            #path + os.sep + 
            if len(line.strip()) == 0:
            #防止line为'\n'字符串
                continue
            stats = pysvn.st(line.strip())
            #line可能不存在，所以需要判断
            if len(stats) == 0:
                continue
            else:
                stat = stats[0]
            varpath = line.strip().split()[-1].strip()
            if stat.find('?') == 0 or stat.find('A') == 0:
                if stat.find('A') == 0:
                    pysvn.py_cmd.command_str = 'svn revert "' + varpath + '"'
                    pysvn.py_cmd.is_cmd_succeeded()
                if sys.platform.find("linux") > -1:
                    pysvn.py_cmd.command_str = 'rm -rf "' + varpath + '"'
                elif sys.platform.find("win") > -1:
                    if os.path.isfile(varpath):
                        pysvn.py_cmd.command_str = 'del /F /Q "' + varpath + '"'
                    else:
                        pysvn.py_cmd.command_str = 'rmdir /S /Q "' + varpath + '"'
                else:
                    pysvn.py_cmd.command_str = ""
            elif len(stat) > 0:
                pysvn.py_cmd.command_str = 'svn revert "' + varpath + '"'
            else:
                pysvn.py_cmd.command_str = ""
            pysvn.py_cmd.is_cmd_succeeded()
                    
    @staticmethod
    def commit_all(path, username, password, filefullname, isfile=True):
        """if isfile, filefullname is full log file name, otherwise, is a message content"""
        lines = pysvn.st(path)
        for line in lines:
            if line.find('?') == 0:
                pysvn.py_cmd.command_str = 'svn add "' + line.replace('?','',1).strip() + '"'
            elif line.find('!') == 0:
                pysvn.py_cmd.command_str = 'svn del "' + line.replace('!','',1).strip() + '"'
            else:
                pysvn.py_cmd.command_str = ""
            pysvn.py_cmd.is_cmd_succeeded()
        if isfile:
            pysvn.py_cmd.command_str = "svn commit -F \"" + filefullname + "\" \"" + path + "\"" + " " + " --username " + username + " --password " + password + " --trust-server-cert " + "--non-interactive"
        else:
            pysvn.py_cmd.command_str = "svn commit -m \"" + filefullname + "\" \"" + path + "\"" + " " + " --username " + username + " --password " + password + " --trust-server-cert " + "--non-interactive"
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_all())
    
    @staticmethod
    def commit_targets(path, targets, username, password, filefullname, isfile=True):
        """
        if isfile, filefullname is full log file name, otherwise, is a message content
        targets is a file path that contained files and directories which will be commited 
        """
        #import pdb
        #pdb.set_trace()
        os.chdir(path);
        f = open(targets, 'r')
        lines = f.readlines()
        f.close()
        if len(lines) == 0:
            print(targets + "内容为空，没有内容需要提交。")
            return("")
        for line in lines:
            #path + os.sep + 
            if len(line.strip()) == 0:
            #防止line为'\n'字符串
                continue
            stat = pysvn.st(line.strip())
            if len(stat) > 0:
                if stat[0].find('?') == 0:
                    pysvn.py_cmd.command_str = 'svn add "' + stat[0].replace('?','',1).strip() + '"'
                elif stat[0].find('!') == 0:
                    pysvn.py_cmd.command_str = 'svn del "' + stat[0].replace('!','',1).strip() + '"'
                else:
                    pysvn.py_cmd.command_str = ""
                pysvn.py_cmd.is_cmd_succeeded()
        '''
        lines = pysvn.st(path)
        for line in lines:
            if line.find('?') == 0:
                pysvn.py_cmd.command_str = 'svn add "' + line.replace('?','',1).strip() + '"'
            elif line.find('!') == 0:
                pysvn.py_cmd.command_str = 'svn del "' + line.replace('!','',1).strip() + '"'
            else:
                pysvn.py_cmd.command_str = ""
            pysvn.py_cmd.is_cmd_succeeded()
        '''
        if isfile:
            pysvn.py_cmd.command_str = "svn commit -F \"" + filefullname + "\" " + "--targets \"" + targets + "\" " + " --username " + username + " --password " + password + " --trust-server-cert " + "--non-interactive"
        else:
            pysvn.py_cmd.command_str = "svn commit -m \"" + filefullname + "\" " + "--targets \"" + targets + "\" " + " --username " + username + " --password " + password + " --trust-server-cert " + "--non-interactive"
        pysvn.py_cmd.is_cmd_succeeded()
        return(pysvn.py_cmd.get_stdout_all())

if __name__ == '__main__':   
    print("hello")
    info_out = pysvn.info("https://007.5173.com/svn/SourceCode/AskDev/Release/partner/2012年3月/partner_20120308_I", "301645", "//5173@#q")
    compile_pattern = re.compile("Revision:\s+\d+", re.I)
    all_groups = re.findall(compile_pattern, info_out)
    print(all_groups)
    pysvn.list("https://007.5173.com/svn/SourceCode/AskDev/Release/partner/2012年3月/partner_20120308_I", "301645", "//5173@#q")
    pysvn.log("https://007.5173.com/svn/SourceCode/AskDev/Release/partner/2012年3月/partner_20120308_I", "301645", "//5173@#q")
    print(pysvn.py_get_log_message("https://007.5173.com/svn/SourceCode/AskDev/Release/partner/2012年3月/partner_20120308_I", "301645", "//5173@#q"))
    print(pysvn.py_get_svn_info_revision("https://007.5173.com/svn/SourceCode/AskDev/Release/partner/2012年3月/partner_20120308_I", "301645", "//5173@#q"))
    print(pysvn.py_get_svn_info_url("https://007.5173.com/svn/SourceCode/AskDev/Release/partner/2012年3月/partner_20120308_I", "301645", "//5173@#q"))
    
    #print(info_out)
#    pdb.set_trace()
#    pysvn.clear_workingcopy_by_targets(r'E:\test', r'E:\test\changelist.txt')
#   pysvn.commit_targets(r"e:\test", r"e:\changelist.txt", "liubin", "liubin0627", r"test commit_targets", False)
#pysvn.clear_workingcopy(r"e:\test")
        