'''
Created on 2011-12-20

@author: 301645
'''
from common.pysvn import pysvn
from common.pywincmd import pywincmds
import os
from common.pyemail import pyemail
from common.pyupdate_three import pyupdate_three

username = "301645"
password = "//5173@#q"
username_online = "zhangyfsh"
password_online = "hjqipS5u95"
svn_url = os.getenv("svn_url")
svn_revision = os.getenv("svn_revision")
site_name = os.getenv("site_name")
site_path = os.getenv("site_path")
phase = os.getenv("phase")
workspace = os.getenv("WORKSPACE");
to_list = os.getenv("to_list").split(',')
#message为日志信息
message = os.getenv("message")
hudson_url = "http://192.168.3.130:8080/hudson/job/"
log_url = hudson_url + os.path.basename(workspace) + "/" + os.getenv('BUILD_NUMBER') + r"/console"

apppool = os.getenv("apppool")
sit_url = os.getenv("site_url")
site_keyword = os.getenv("site_keyword", "OK")
inteveral_time = 100
web_decode = "gb2312"

co_path = workspace + os.sep + "update_packs"
changelist = workspace + os.sep + "changlist.txt"
url_file = workspace + os.sep + "url_file.txt"
release_notes_url = os.getenv("release_notes_url")
release_notes_local_path = workspace + os.sep + "release_notes"

def update_3(flag):
    '''
    py_file需要全局变量, pyfile不能在co_path内
    co_path为更新包路径检出位置
    py_file为更新文件列表存放文件
    '''
    global svn_revision
    pysvn.up("HEAD", site_path, username_online, password_online)
    if os.path.exists(co_path):
        pywincmds.del_dir(co_path)
    pysvn.co(svn_url, svn_revision, co_path, username, password)
    list_tree = pysvn.list_agile('svn list -R', svn_url, username, password)
    for i in range(0,len(list_tree)):
        list_tree[i] = list_tree[i].lower().strip().rstrip("/")
    list_tree_actual = []              
    pywincmds.py_write_svn_message_to_file(svn_url, url_file)
    pywincmds.py_robocopy(co_path, site_path, '.svn _svn', '')
    os.chdir(site_path)
    st = pysvn.st("") #更新文件列表
    #使用svn list url和svn st产生列表的分隔符不一致，下面的方法只适用于windows
    for item in st:
        try:
            if list_tree.index(item.strip().split()[-1].strip().replace("\\", "/").lower()) > -1:
                list_tree_actual.append(item.strip().split()[-1].strip().replace("\\", "/"))
        except:
            pass
    if len(list_tree_actual) == 0:
        print("无更新内容！")
        exit(1)
    list_str = '\n'.join(list_tree_actual).strip()
    pywincmds.py_write_svn_message_to_file(list_str, changelist)
    if flag:
        pywincmds.restart_app_pool(workspace + os.sep + "sbp", apppool)
    if pywincmds.web_check(sit_url, site_keyword, inteveral_time, web_decode):
        #三段启动成功
        svn_revision = pysvn.py_get_svn_info_revision(pysvn.info(co_path, username, password))
        content = "更新包url：" + svn_url + "\n" + "更新包版本：" + svn_revision + "\n\n"
        content = content + "三段差异内容：" + "\n"
        content = content + '\n'.join(st).strip()
        content = content + "\n" + "详情见：" + "\n" + log_url
        title = site_name + "三段更新成功，请测试，谢谢！"
        #邮件
        pyemail.send(to_list, title, content, [])

#scm可以先行更新三段，待收到三段更新邮件通知后，再通知测试，在时间紧张的时候使用
def update_3_resend_email():
    os.chdir(site_path)
    st = pysvn.st("") #更新文件列表
    if pywincmds.web_check(sit_url, site_keyword, inteveral_time, web_decode):
        #三段启动成功
        svn_revision = pysvn.py_get_svn_info_revision(pysvn.info(co_path, username, password))
        content = "更新包url：" + svn_url + "\n" + "更新包版本：" + svn_revision + "\n\n"
        content = content + "三段差异内容：" + "\n"
        content = content + '\n'.join(st).strip()
        content = content + "\n" + "详情见：" + "\n" + log_url
        title = site_name + "三段更新成功，请测试，谢谢！"
        #邮件
        pyemail.send(to_list, title, content, [])

def revert():
    pysvn.clear_workingcopy_by_targets(site_path, changelist)
    st = pysvn.st(site_path)
    title = site_name + "三段回滚成功，谢谢！"
    content = "三段站点状态：" + '\n' + '\n'.join(st).strip()
    pyemail.send(to_list, title, content, [])

def commit():
    global release_notes_url
    title = site_name + "三段测试通过，请更新线上服务器，谢谢！"
    if release_notes_url == None:
        f = open(url_file)
        svn_url = f.readlines()[0].strip()
        release_notes_url = os.path.dirname(svn_url)
        try:
            if svn_url.rindex('/') == len(svn_url) - 1 or  svn_url.rindex('\\') == len(svn_url):
                release_notes_url = os.path.dirname(release_notes_url)
        except:
            pass
        f.close()
    pt = pyupdate_three()
    sourcecode = {"username":username, "password":password}
    release_notes_file = pt.get_release_notes_path(release_notes_url, sourcecode, release_notes_local_path)
    commit_content = pysvn.commit_targets(site_path, changelist, username_online, password_online, message, isfile=False)
    content = "各位好：" + "\n" + "三段测试通过，请更新线上服务器，谢谢！" + "\n" + "提交内容为：" + "\n" + commit_content + "\n"
    content = content + "日志信息：\n" + message
    content = content + "\n" + "详情见：" + "\n" + log_url
    if release_notes_file == None:
        pyemail.send(to_list, title, content, [])
    else:
        pyemail.send(to_list, title, content, [release_notes_file])
    st = pysvn.st(site_path)
    pyemail.send(["scm@5173.com"], site_name + "站点目录当前内容如下，便于检查", '\n'.join(st).strip() + " ", [])

def recycle_apppool():
    pywincmds.restart_app_pool(workspace + os.sep + "sbp", apppool)
    if pywincmds.web_check(sit_url, site_keyword, inteveral_time, web_decode):
        pyemail.send(to_list, site_name + "三段启动成功！", " ", [])
    else:
        exit(1)

def view_host():
    windir = os.getenv("windir", r"C:\WINDOWS")
    f=open(windir + os.sep + r"system32\drivers\etc\hosts")
    lines = f.readlines()
    for line in lines:
        print(line)
    f.close()
    
def revert_to_revision():
    #回滚到某个版本
    os.chdir(site_path)
    pre_st = pysvn.st("")
    pass

if phase == "update_3":
    update_3(True)
elif phase == "update_3_without_recycling_apppool":
    update_3(False)
elif phase == "revert":
    revert()
elif phase == "commit":
    commit()
elif phase == "recycle_apppool":
    recycle_apppool()
elif phase == "view_host":
    view_host()
elif phase == "update_3_resend_email":
    update_3_resend_email()
