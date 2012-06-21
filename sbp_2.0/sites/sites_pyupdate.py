'''
Created on 2011-12-20

@author: 301645
'''
from common.pysvn import pysvn
from common.pywincmds import pywincmds
import os
from common.pyemail import pyemail
from common.pyupdate3 import pyupdate3
from common.pyproperties import pyproperties
from sites.sites_pybuild import build_and_update_common
from common.pyprocessemail import pyprocessemail

class sites_pyupdate(pyupdate3, build_and_update_common):
    def __init__(self, site):
        self.workspace = os.getenv("WORKSPACE", r"D:\Documents and Settings\binliu\workspace")#self.home)
        self.revision = os.getenv("revision", "HEAD")
        self.full_site_name = os.getenv("site_name", "ALL")
        self.common_p = pyproperties(self.workspace + r"\sbp_2.0\sites\common.config.yaml").get_dict()
        self.private_p = pyproperties(self.workspace + r"\sbp_2.0\sites" + os.sep + site + os.sep + self.full_site_name +  r"_update.config.yaml").get_dict()
        self.product_tag_url = self.private_p["product_url"] + "/tags/" + self.full_site_name
        self.product_trunk_url = self.private_p["product_url"] + "/trunk/" + self.full_site_name
        self.product_tag_dir = self.workspace + os.sep + self.private_p["product_tag_dir"]
        self.product_trunk_dir = self.workspace + os.sep + self.private_p["product_trunk_dir"]
        self.changelist = self.product_trunk_dir + os.sep + "changelist.txt"
        self.sourcecode_username = self.get_property("sourcecode_username")
        self.sourcecode_password = self.get_property("sourcecode_password")
        self.product_username = self.get_property("product_username")
        self.product_password = self.get_property("product_password")
        self.online_username = self.get_property("online_username")
        self.online_password = self.get_property("online_password")
        self.online_site_path = self.private_p["online_site_path"]
        self.app_pool = self.private_p["app_pool"]
        self.website_verified_url = self.private_p["website_verified_url"]
        self.verified_keyword = self.private_p["verified_keyword"]
        self.inteveral_time = 100
        self.web_decode = "gb2312"
        self.temp_changelist = self.workspace + os.sep + "changlist.txt"
        self.to_list = os.getenv("to_list", "scm")
        self.hudson_url = "http://192.168.3.130:8080/hudson/job/"
        self.log_url = self.hudson_url + os.path.basename(self.workspace) + "/" + os.getenv('BUILD_NUMBER', "100") + r"/console"
        #self.message = os.getenv("message", time.strftime("%y-%m-%d",time.localtime()))
        self.py_log_file = self.workspace + os.sep + "py_log_file.txt"
        self.release_notes_local_path = self.workspace + os.sep + "release_notes"
        self.release_notes_url = os.getenv("release_notes_url")
        
    def check_sourcecode(self):
        if os.path.exists(self.product_tag_dir):
            pysvn.clear_workingcopy(self.product_tag_dir)
        self.co_path(self.product_tag_url, self.product_tag_dir, self.product_username, self.product_password, "HEAD")
        self.co_path(self.product_trunk_url, self.product_trunk_dir, self.product_username, self.product_password, self.revision)
        pysvn.up(self.online_site_path,  self.online_username, self.online_password)
    
    def del_files(self, path):
        f = open(self.changelist)
        lines = f.readlines()
        f.close()
        changelines = []
        os.chdir(path)
        for line in lines:
            if line.strip() != "" and line.strip().find("!") == 0:
                file_path = line.strip().split()[-1].strip()
                try:
                    pysvn.delete(file_path)
                except Exception as e:
                    print(file_path + ":" , e)
            if  line.strip() != "":
                changelines.append(line.strip().split()[-1].strip())
        pywincmds.py_write_svn_message_to_file(os.linesep.join(changelines), self.temp_changelist)
        
    def update(self, flag = True):
        self.check_sourcecode()
        pywincmds.del_all_except_hidden_directories(self.product_tag_dir)
        pywincmds.robocopy(self.product_trunk_dir, self.product_tag_dir, py_exclude_dirs = ".svn _svn config Config_online log", py_exclude_files = "web.config changelist.txt revision_numbers.txt")
        pywincmds.robocopy(self.product_trunk_dir + os.sep + "Config_online", self.product_tag_dir, py_exclude_dirs = ".svn _svn")
        self.del_files(self.product_tag_dir)
        pywincmds.robocopy(self.product_tag_dir, self.online_site_path, py_exclude_dirs = ".svn _svn Config_online log", py_exclude_files = "changelist.txt revision_numbers.txt")
        self.del_files(self.online_site_path)
        if flag:
            pywincmds.restart_app_pool(self.workspace + os.sep + "sbp_2.0", self.app_pool)
        if pywincmds.web_check(self.website_verified_url, self.verified_keyword, self.inteveral_time, self.web_decode):
            os.chdir(self.online_site_path)
            updated_content = os.linesep.join(pysvn.st(""))
            pyprocessemail.update_to_three(self.full_site_name, self.to_list, self.product_trunk_url, pysvn.py_get_svn_info_revision(self.product_trunk_dir, self.product_username, self.product_password), updated_content, self.log_url)
        else:
            print("站点启动失败")
            exit("1")

    def resend_email(self):
        if pywincmds.web_check(self.website_verified_url, self.verified_keyword, self.inteveral_time, self.web_decode):
            os.chdir(self.online_site_path)
            updated_content = os.linesep.join(pysvn.st(""))
            pyprocessemail.update_to_three(self.full_site_name, self.to_list, self.product_trunk_url, pysvn.py_get_svn_info_revision(self.product_trunk_dir, self.product_username, self.product_password), updated_content, self.log_url)
        else:
            print("站点启动失败")
            exit("1")
    
    def revert(self):
        pysvn.clear_workingcopy_by_targets(self.online_site_path, self.temp_changelist)
        st = pysvn.st(self.online_site_path)
        title = self.full_site_name + "三段回滚成功，谢谢！"
        content = "三段站点状态：" + '\n' + '\n'.join(st).strip()
        pyemail.send(self.to_list, title, content)
    
    def commit(self):
        title = self.full_site_name + "三段测试通过，请更新线上服务器，谢谢！"
        os.chdir(self.online_site_path)
        svn_log = pysvn.py_get_log_message(self.product_trunk_dir, self.product_username, self.product_password)
        pywincmds.py_write_svn_message_to_file(svn_log, self.py_log_file)
        release_notes_file = self.get_release_notes_path(self.release_notes_url, self.sourcecode_username, self.sourcecode_password, self.release_notes_local_path)
        commited_content = pysvn.commit_targets(self.online_site_path, self.temp_changelist, self.online_username, self.online_password, self.py_log_file)
        #如果提交内容为空，则不提交。
        if commited_content == "":
            print("提交内容为空")
            exit(1)
        #pyprocessemail.commit_to_online(site, to_list, commited_content, product_test["url"], svn_log, log_url)
        #print("邮件参数为：",site, to_list, commited_content, product_release_revision, svn_log, log_url, release_notes_path)
        content = "各位好：" + "\n" + "三段测试通过，请更新线上服务器，谢谢！" + "\n" + "提交内容为：" + "\n" + commited_content + "\n"
        content = content + "日志信息：\n" + svn_log
        content = content + "\n" + "详情见：" + "\n" + self.log_url
        if release_notes_file == None:
            pyemail.send(self.to_list, title, content, [])
        else:
            pyemail.send(self.to_list, title, content, [release_notes_file])
        st = pysvn.st(self.online_site_path)
        pyemail.send("scm@5173.com", self.full_site_name + "站点目录当前内容如下，便于检查", '\n'.join(st).strip())
        
    def make_label(self):
        title = self.full_site_name + "标签已打，谢谢！"
        os.chdir(self.product_tag_dir)
        svn_log = pysvn.py_get_log_message(self.online_site_path, self.online_username, self.online_password)
        pywincmds.py_write_svn_message_to_file(svn_log, self.py_log_file)
        commited_content = pysvn.commit_all(self.product_tag_dir, self.product_username, self.product_password, self.py_log_file)
        if commited_content == "":
            print("提交内容为空")
            exit(1)
        pyemail.send(self.to_list, title, commited_content)
        st = pysvn.st(self.product_tag_dir)
        pyemail.send("scm@5173.com", self.full_site_name + "标签内容如下，便于检查", '\n'.join(st).strip())