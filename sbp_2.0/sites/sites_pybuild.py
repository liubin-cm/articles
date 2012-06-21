'''
Created on 2012-3-12

@author: 301645
'''
import os
import re
import time
import yaml
from common.pybuild import pybuild
from common.pyproperties import pyproperties
from common.pysvn import pysvn
from common.pywincmds import pywincmds
from common.pyprocessemail import pyprocessemail
from common.pyemail import pyemail

class build_and_update_common(object):
    def get_property(self, key):
        if self.private_p.get(key) != None:
            return(self.private_p.get(key))
        if self.common_p.get(key) != None:
            return(self.common_p.get(key))
        return(None)
        
    def add_pre_for_arr(self, string, arr, is_sub = False):
        length = len(arr)
        if is_sub:
            res =[]
            for i in range(0,length):
                res.append(string + arr[i])
            return(res)
        else:
            for i in range(0,length):
                arr[i] = string + arr[i]
            return(arr)
    
    def convert_str_to_list(self, value):
        if isinstance(value, list):
            return(value)
        elif isinstance(value, str):
            return([value])
    
    def co_path(self, urls, dirs, username, password, revision="HEAD"):
        if isinstance(urls, list):
            length = len(urls)
            for j in range(0, length):
                if os.path.exists(dirs[j]):
                    pysvn.up(dirs[j], username, password, revision)
                else:
                    pysvn.co(urls[j], dirs[j], username, password, revision)
        elif isinstance(urls, str):
            if os.path.exists(dirs):
                    pysvn.up(dirs, username, password, revision)
            else:
                pysvn.co(urls, dirs, username, password, revision)

    def substitute(self, src, dst):
        if not os.path.exists(src):
            print(src + "不存在！")
            return
        try:
            if os.path.isdir(dst):
                pywincmds.del_dir(dst)
                pywincmds.robocopy(src, dst)
            elif os.path.isfile(dst):
                pywincmds.copy(src, dst)
        except Exception as e:
            print(e)
    
    def get_release_notes_path(self, updated_package_url, username, password, local_path):
        '''
                    获取版本说明路径，包括几个步骤：
        1、下载版本说明到本地路径
        2、返回本地路径
        '''
        if updated_package_url == None:
            print("请填写版本说明父目录url")
            return(None)
        if os.path.exists(local_path):
            pywincmds.del_dir(local_path)
        #print("svn co --depth files", updated_package_url, revision, local_path, sourcecode["username"], sourcecode["password"])
        pysvn.co(updated_package_url, local_path, username, password, depth="files")
        files = os.listdir(local_path)
        release_notes_path = ""
        for file in files:
            if file.find("版本说明") > -1:
                new_file = (local_path + os.sep + file).replace('版本说明', 'release_notes', 1)
                os.rename(local_path + os.sep + file, new_file)
                release_notes_path = new_file
        if not release_notes_path:
            print("版本说明路径不对，请重新输入")
            exit(1)
        else:
            return(release_notes_path)
        
class sites_pybuild(pybuild, build_and_update_common):
    '''
    classdocs
    '''
    def __init__(self, site):
        '''
        Constructor
        '''
        self.home = os.getenv("HOME", "C:\\Documents and Settings\\301645")
        self.workspace = os.getenv("WORKSPACE", r"C:\hudson\workspace\gameid_build_new")#self.home)
        self.revision = os.getenv("revision", "HEAD")
        self.is_need_build = os.getenv("is_need_build", "true")
        self.common_p = pyproperties(self.workspace + r"\sbp_2.0\sites\common.config.yaml").get_dict()
        self.private_p = pyproperties(self.workspace + r"\sbp_2.0\sites" + os.sep + site + os.sep + site +  r"_build.config.yaml").get_dict()
        #self.site_names = self.private_p.get_property("site_names")
        self.sourcecode_urls = self.private_p["sourcecode_urls"]
        self.sourcecode_dirs = self.add_pre_for_arr(self.workspace + os.sep, self.private_p["sourcecode_dirs"], True)
        self.sourcecode_username = self.get_property("sourcecode_username")
        self.sourcecode_password = self.get_property("sourcecode_password")
        self.sourcecode_dir = self.sourcecode_dirs[0]
        self.build_batch = self.workspace + os.sep + self.private_p["build_batch"]
        #self.copy_bats = self.add_pre_for_arr(self.sourcecode_dir + os.sep, self.private_p["copy_batches"], True)
        self.full_site_name = os.getenv("site_name", "ALL")
        self.sites = self.private_p["sites"]    
        self.product_username = self.get_property("product_username")
        self.product_password = self.get_property("product_password")
        self.online_username = self.get_property("online_username")
        self.online_password = self.get_property("online_password")
        self.getversion_exe = self.workspace + os.sep + self.private_p["GetVersion"]
        self.sourcecode_st = ""

        self.to_list = os.getenv("to_list", "liubin")
        self.hudson_url = "http://192.168.3.130:8080/hudson/job/"
        self.log_url = self.hudson_url + os.path.basename(self.workspace) + "/" + os.getenv('BUILD_NUMBER', "100") + r"/console"
        self.message = os.getenv("message", time.strftime("%y-%m-%d",time.localtime()))
        self.py_log_file = self.workspace + os.sep + "py_log_file.txt"
            
    def checkout_source(self):
        self.co_path(self.sourcecode_urls, self.sourcecode_dirs, self.sourcecode_username, self.sourcecode_password, self.revision)
        if self.full_site_name == "ALL":
            for key in self.sites.keys():
                self.co_path(self.sites[key]["product_url"], self.workspace + os.sep + self.sites[key]["product_dir"], self.product_username, self.product_password)
                pysvn.clear_workingcopy(self.workspace + os.sep + self.sites[key]["online_dir"])
                self.co_path(self.sites[key]["online_url"], self.workspace + os.sep + self.sites[key]["online_dir"], self.online_username, self.online_password)
        else:
            self.co_path(self.sites[self.full_site_name]["product_url"], self.workspace + os.sep + self.sites[self.full_site_name]["product_dir"], self.product_username, self.product_password)
            pysvn.clear_workingcopy(self.workspace + os.sep + self.sites[self.full_site_name]["online_dir"])
            self.co_path(self.sites[self.full_site_name]["online_url"], self.workspace + os.sep + self.sites[self.full_site_name]["online_dir"], self.online_username, self.online_password)
        '''
        for i in self.sourcecode_dirs:
            self.sourcecode_st = self.sourcecode_st + "\r\n" + pysvn.st(i)
        
        self.sourcecode_st = self.sourcecode_st + "\r\n" + pysvn.st(self.product_dir)
        
        for j in self.online_dirs:
            self.sourcecode_st = self.sourcecode_st + "\r\n" + pysvn.st(j)
        '''
    def build(self):
        if self.is_need_build == "true":
            pywincmds.call_cmd(self.build_batch + " " + os.getenv("build_type","Build"))
        pass

    def change_email(self, site_name):
        online_dir = self.workspace + os.sep + self.sites[site_name]["online_dir"]
        site_dir = self.workspace + os.sep +  self.sites[site_name]["site_dir"]
        os.chdir(online_dir)
        lines = pysvn.st("")
        contents = []
        for line in lines:
            path = site_dir + os.sep + line.strip().split()[-1].strip() #line.replace(line[0],'',1).strip()
            if path.lower().find(r'.dll') > -1 or path.lower().find(r'.pdb') > -1 or path.lower().find(r'.txt') > -1:
                contents.append(line)
            else:
                try:
                    log_summary = pysvn.log(path, self.sourcecode_username, self.sourcecode_password,quite="-q")
                    compiled_pattern = re.compile("r.*", re.M)
                    log_summary = re.search(compiled_pattern, log_summary).group().strip()
                    if log_summary.find("|") > -1:                
                        log_items = log_summary.split("|")
                        contents.append(log_items[2].strip() + "    " +  log_items[1].strip() + "    " + line)#"{0:<80},{1}".format(line, log_summary))
                    else:
                        contents.append(log_summary)
                except:
                    contents.append(line)
        contents.sort()
        updated_content = os.linesep.join(contents)
        pyprocessemail.build_success(site_name, self.to_list, pysvn.py_get_svn_info_url(site_dir, self.sourcecode_username, self.sourcecode_password), pysvn.py_get_svn_info_revision(site_dir, self.sourcecode_username, self.sourcecode_password), updated_content, self.log_url)
    
    def send_email_for_site(self, site_name):
        site_dir = self.workspace + os.sep + self.sites[site_name]["site_dir"]
        online_dir = self.workspace + os.sep + self.sites[site_name]["online_dir"]
        pywincmds.call_cmd("echo " + self.workspace + os.sep + self.sites[site_name]["online_dir"] + "|" + self.workspace + os.sep + self.sites[site_name]["copy_bat"])
        self.substitute(site_dir + os.sep + "config_online" + os.sep + self.sites[site_name]["web_config"]["config_online"], online_dir + os.sep + self.sites[site_name]["web_config"]["online"])
        self.substitute(site_dir + os.sep + "config_online" + os.sep + "config", online_dir + os.sep + self.sites[site_name]["config"])
        self.change_email(site_name)
        
    def send_email_for_changes(self):
        #length = len(self.site_names)
        if self.full_site_name == "ALL":
            for key in self.sites.keys():
                self.send_email_for_site(key)
        else:
            self.send_email_for_site(self.full_site_name)
        pass
  
    def commit_offline(self,site_name):
        product_dir = self.workspace + os.sep + self.sites[site_name]["product_dir"]
        online_dir = self.workspace + os.sep + self.sites[site_name]["online_dir"]
        site_dir = self.workspace + os.sep +  self.sites[site_name]["site_dir"]
        pywincmds.del_all_except_hidden_directories(product_dir)
        pywincmds.robocopy(online_dir, product_dir, py_exclude_dirs=".svn _svn")
        try:
            self.substitute(site_dir + os.sep + "config_test" + os.sep + "config", product_dir + os.sep + self.sites[site_name]["config"])
            self.substitute(site_dir + os.sep + "config_test" + os.sep + self.sites[site_name]["web_config"]["config_test"], product_dir + os.sep + self.sites[site_name]["web_config"]["online"])
        except:
            pass
        pywincmds.robocopy(site_dir + os.sep + "config_online", product_dir + os.sep + "Config_online", py_exclude_dirs = ".svn _svn")
        os.chdir(product_dir + os.sep + "Config_online")
        os.rename(self.sites[site_name]["web_config"]["config_online"], self.sites[site_name]["web_config"]["online"])
        os.chdir(online_dir)
        lines = pysvn.st("")
        lines = [line.strip() for line in lines]
        if len(lines) == 0:
            pyemail.send(self.to_list, site_name + "无变化内容", "")
            return
        else:
            pywincmds.py_write_svn_message_to_file("\n".join(lines), product_dir + os.sep + "changelist.txt")
            if os.path.exists(self.getversion_exe):
                pywincmds.call_cmd(self.getversion_exe + " \"" + self.sourcecode_dir + "\"")
                time.sleep(10)
                #pywincmds.copy(self.sourcecode_dir + os.sep + "my_version.txt", self.product_dir + os.sep + self.site_names[site_name] + os.sep + "revision_numbers.txt")
            svn_log_message = "sourcecode : " + pysvn.py_get_svn_info_url(site_dir, self.sourcecode_username, self.sourcecode_password) + '\n' + "version number : " + pysvn.py_get_svn_info_revision(site_dir, self.sourcecode_username, self.sourcecode_password) + '\n'
            svn_log_message = svn_log_message + "main updated contents : " + '\n' + self.message
            pywincmds.py_write_svn_message_to_file(svn_log_message, self.py_log_file)
            updated_content = pysvn.commit_all(product_dir, self.product_username, self.product_password, self.py_log_file)
            pyprocessemail.commit_to_product(site_name, self.to_list, updated_content, self.sites[site_name]["product_url"], svn_log_message, self.log_url)
                        
    def send_email_for_commit(self):
        if self.full_site_name == "ALL":
            for key in self.sites.keys():
                self.commit_offline(key)
        else:
            self.commit_offline(self.full_site_name)
            pass
    
if __name__ == '__main__':  
    pysvn.up(r"C:\hudson\workspace\gameid_build_new\sbp_2.0", "301645", "//5173@#q")
    p = sites_pybuild("gameid")
    #print(p.site_names)
    print(p.build_batch)
    #print(p.copy_bats)
    #print(p.sites_src_dirs)
    #print(p.online_urls)
    #print(p.online_dirs)
    print(p.sourcecode_username, p.sourcecode_password)
    print(p.product_password)
    print(p.sourcecode_dirs)
    print(p.getversion_exe)
    #print(p.product_url)
    #print(p.product_dir)
    for key in p.sites.keys():
        print(p.sites[key])
    print(p.sourcecode_dirs)
    print(p.sourcecode_urls)
    print(p.revision)
    phase = "commit"
    if phase == "build":
        p.checkout_source()
        p.build()
        p.send_email_for_changes()
    elif phase == "commit":
        p.send_email_for_commit()
    elif phase == "build_and_commit":
        p.checkout_source()
        p.build()
        p.send_email_for_changes()
        p.send_email_for_commit()
 