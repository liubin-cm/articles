'''
Created on 2012-3-13

@author: 301645
'''
import os
import shutil
from common.pyruncmd import pyruncmd
class pywincmds(object):
    '''
    封装一些经常使用的windows命令
    '''
    py_cmd = pyruncmd()
          
    @staticmethod
    def call_cmd(py_curcmd):
        pywincmds.py_cmd.command_str = py_curcmd
        pywincmds.py_cmd.is_cmd_succeeded()
        
    @staticmethod
    def makedirs(absolute_path):
        os.makedirs(absolute_path, exist_ok=True)
    
    @staticmethod
    def copy_make_parentedirs(src, dst):
        #=======================================================================
        # 拷贝文件，如果des上层目录不存在，则新建目录
        #des需要含有文件名
        #=======================================================================
        par_dir = os.path.dirname(dst).strip() 
        if not os.path.exists(par_dir):
            pywincmds.makedirs(par_dir)
        if os.path.exists(src):
            shutil.copy2(src, dst)
        
    @staticmethod
    def robocopy(py_source, py_dest, pyfiles = "", py_exclude_dirs="", py_exclude_files=""):
        """排除文件目录可以就模式，如/XD .svn obj config Properties "Web References" /XF *.cs *.csproj *.pdb *.resx *.csproj.user"""   
        if not os.path.exists(py_source):
            raise("源文件" + py_source + "不存在！")
        files = xd = xf = ""
        robocopy_path = os.getenv("WORKSPACE", r"D:\Documents and Settings\binliu\workspace") + os.sep + "sbp_2.0" + os.sep + "tools" + os.sep + "robocopy"
        if pyfiles.strip() != "":
            files = " " + pyfiles + " " 
        if py_exclude_dirs.strip() != "":
            xd = " /XD " + py_exclude_dirs + " "
        if py_exclude_files.strip()!="":
            xf = " /XF " + py_exclude_files + " "
        pywincmds.py_cmd.command_str = "\"" + robocopy_path + "\"" + " \"" + py_source + "\" \"" + py_dest + "\"" + files + xd + xf + " /E"
        pywincmds.py_cmd.is_cmd_succeeded(7)
    
    @staticmethod  
    def copy(py_source, py_dest):
        '''
        拷贝单个文件
        '''
        if not os.path.exists(py_source):
            raise("源文件" + py_source + "不存在！")
        pywincmds.py_cmd.command_str = "copy \"" + py_source + "\" \"" + py_dest + "\" /Y"
        pywincmds.py_cmd.is_cmd_succeeded()
        
    @staticmethod
    def del_dir(py_dir):
        '''
                    删除目录py_dir，即使它包含子目录和文件
        '''
        try:
            if os.path.isdir(py_dir):
                shutil.rmtree(py_dir)
        except Exception as e:
            raise(e)
        
    @staticmethod    
    def del_all_except_hidden_directories(py_dir_root):
        """删除除.svn的其他文件和目录"""    
        pywincmds.py_cmd.command_str = "dir /B \"" + py_dir_root + "\""
        pywincmds.py_cmd.is_cmd_succeeded()
        lists = pywincmds.py_cmd.get_stdout_lines()
        for line in lists:
            if os.path.isfile(py_dir_root + os.sep + line.strip()):
                pywincmds.py_cmd.command_str = 'del /F /Q "' + py_dir_root + os.sep + line.strip() + '"'
            else:
                pywincmds.py_cmd.command_str = 'rmdir /S /Q "' + py_dir_root + os.sep + line.strip() + '"'
            pywincmds.py_cmd.is_cmd_succeeded()
            
    @staticmethod
    def py_write_svn_message_to_file(py_message, py_file):
        """多行需要以\n分隔而不是\r\n"""
        if os.path.exists(py_file):
            os.system("del  /F /Q \"" + py_file + "\"")
        f = open(py_file, 'w')
        f.write(py_message)
        f.close()
    
    @staticmethod
    def restart_app_pool(cur_file_path, py_apppool):
        import platform
        if platform.release().find("2008Server") > -1:
            pywincmds.py_cmd.command_str = r"C:\Windows\SysWOW64\inetsrv\appcmd.exe recycle apppool " + py_apppool
        else:    
            pywincmds.py_cmd.command_str = "\"" + cur_file_path + os.sep + "tools" + os.sep + "cscript.exe\" \"" + cur_file_path + os.sep + "tools" + os.sep + "iisapp.vbs\" /a " + py_apppool + " /r" 
        pywincmds.py_cmd.is_cmd_succeeded()
    
    @staticmethod
    def web_check(py_url, py_keyword, py_time, py_decode):
        #time in seconds
        #其中py_url为检测的地址，py_keyword为搜索的关键字，py_time为间隔时间，总的间隔时间为60*py_time seconds, 如果发现，返回真，否则为假
        #py_decode为编码，比如gb2312，为字符串
        import time
        import urllib.request
        for i in range(0,60):
            time.sleep(float(py_time)) 
            req = urllib.request.urlopen(py_url,timeout=180)
            content = req.readall()
            page=""
            try:
                page = str(content, py_decode)
            except:
                req = urllib.request.urlopen(py_url,timeout=180)
                if py_decode == "utf-8":
                    page = str(content, "gb2312")
                else:
                    page = str(content, "utf-8")
            if page.find(py_keyword) > -1:
                return(True)
        return(False)

if __name__ == 'main':  
    pywincmds.list_all_children(r'E:\sourcecode\51tao')
    pywincmds.py_robocopy(r'E:\sourcecode\51tao\WebUI', r'E:\sourcecode\51tao\WebUI1', r'obj', r'*.dll')