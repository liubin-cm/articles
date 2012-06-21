'''
Created on 2011-12-20

@author: 301645
'''
import datetime,time
from common.pysvn import pysvn
from common.pywincmd import pywincmds
import os
from common.pyemail import pyemail
import pdb

workspace = os.getenv("WORKSPACE",r"c:\hudson\workspace\update_style")
phase = os.getenv("phase","commit")
#压缩程序路径
compress_png_path = r"C:\MINI\PNG批量压缩\pngout.exe"
compress_js_paths = [r"C:\MINI\IMAGES001.5173cdn.com.exe", r"C:\MINI\IMAGES002.5173cdn.com.exe", r"C:\MINI\IMAGES.5173cdn.com.exe"]
change_url = "https://192.168.140.28/svn_product/updatestyle"
change_revision = os.getenv("revision", "HEAD")
change_workingcopy = workspace + os.sep + "style_change"
change_username = "301645"
change_password = "//5173@#q"

style_urls = [r"http://images001.5173cdn.com", r"http://images002.5173cdn.com", r"https://images002.5173cdn.com",
             r"http://images.5173cdn.com", r"http://img01.5173cdn.com"]
style_offline_woringcopy = [r"C:\projectin\IMAGES001.5173cdn.com", r"C:\projectin\IMAGES002.5173cdn.com", 
                            r"C:\projectin\IMAGES002.5173cdn.com", r"C:\projectin\IMAGES.5173cdn.com", 
                            r"C:\projectin\IMAGES001.5173cdn.com\tags"]
style_offline_username = "user196"
style_offline_password = "user196"

style_online_woringcopy = [r"C:\project\IMAGES001.5173cdn.com", r"C:\project\IMAGES002.5173cdn.com", 
                            r"C:\project\IMAGES002.5173cdn.com", r"C:\project\IMAGES.5173cdn.com", 
                            r"C:\project\IMAGES001.5173cdn.com\tags"]
style_online_wks = [r"C:\project\IMAGES001.5173cdn.com", r"C:\project\IMAGES002.5173cdn.com", r"C:\project\IMAGES.5173cdn.com"]

style_online_username = os.getenv("style_online_username", "zhangyfsh")
style_online_password = os.getenv("style_online_password", "9MHF774Q0WDAFH2")


if os.path.exists(change_workingcopy):
    pysvn.up(change_revision, change_workingcopy, change_username, change_password)
else:
    pysvn.co(change_url, change_revision, change_workingcopy, change_username, change_password)

urls = []
offline_paths = []
online_paths = []
content = pysvn.log_path(change_workingcopy + os.sep + "change.txt", change_username, change_password)

def url_transfer_path():
    f = open(change_workingcopy + os.sep + "change.txt")
    temp_urls = f.readlines()
    f.close()
    for temp in temp_urls:
        if temp.strip() == "":
            continue
        else:
            urls.append(temp.strip())
    for i in range(0,len(urls)):
        relative_path_index = ""
        for j in range(0,len(style_urls)):
            if urls[i].lower().find(style_urls[j].lower()) > -1:
                relative_path_index = j
                break
        offline_paths.append(urls[i].replace(style_urls[relative_path_index], style_offline_woringcopy[relative_path_index],1).rstrip("/").replace("/", "\\"))
        online_paths.append(urls[i].replace(style_urls[relative_path_index], style_online_woringcopy[relative_path_index],1).rstrip("/").replace("/", "\\"))
        print(offline_paths[i])
        print(online_paths[i])

def update_3():
    #pdb.set_trace()
    #更新样式线下和线上本地拷贝
    for style_offline in style_offline_woringcopy:
        pysvn.up("HEAD", style_offline, style_offline_username, style_offline_password)
    
    for style_online in style_online_woringcopy:
        pysvn.up("HEAD",  style_online, style_online_username , style_online_password)
    #读取文件http列表
    #转换为路径
    url_transfer_path()
    #拷贝文件
    for i in range(0,len(offline_paths)):
        if os.path.isfile(offline_paths[i]):
            pywincmds.makedirs(os.path.dirname(online_paths[i]))
            if os.path.exists(offline_paths[i]):
                pywincmds.py_xcopy_file(offline_paths[i], online_paths[i])
        else:
            pywincmds.py_robocopy(offline_paths[i].rstrip("\\"), online_paths[i].rstrip("\\"), "", "")
    #压缩png文件
    for i in range(0,len(online_paths)):
        if online_paths[i].endswith('.png'):
            try:
                pywincmds.call_cmd(compress_png_path + " \"" + online_paths[i] + "\"")
            except:
                print(online_paths[i] +' error')
            atime = time.mktime(datetime.datetime(2000, 1, 1).utctimetuple())
            mtime = time.mktime(datetime.datetime(2000, 1, 1).utctimetuple())
            os.utime(online_paths[i], (atime, mtime))
            print(online_paths[i])
    #压缩js和css文件
    for compress_js_path in compress_js_paths:
        os.chdir(os.path.dirname(compress_js_path))
        pywincmds.call_cmd(compress_js_path)
        print(compress_js_path)
    #确认已更新，如何确认
    #发送邮件
    pyemail.send(["scm@5173.com"], content.strip() + "样式已更新", " ", [])
    #pass

def commit():
    #pdb.set_trace()
    #读取文件http列表
    url_transfer_path()
    #转换为路径
    #提交路径文件
    #两个工作，将新增的多层目录加到提交列表中，然后分组，按组提交
    commit_arr = [[], [], []]
    all_paths = online_paths[0:len(online_paths)]
    temp_paths = []
    for i in all_paths:
        temp_paths.append(i.lower())
    for online_path in online_paths:
        stat = pysvn.st(online_path.strip())
        if len(stat) == 1:
            if stat[0].find('?') == 0 or stat[0].find('is not a working copy') > -1:
                pysvn.py_cmd.command_str = 'svn add --parents "' + online_path.strip() + '"'
                pysvn.py_cmd.is_cmd_succeeded()
                addoutputs = pysvn.py_cmd.get_stdout_lines()
                for addoutput in addoutputs:
                    addoutput_path = addoutput.replace(addoutput[0],'',1).strip()            
                    try:
                        if temp_paths.index(addoutput_path.lower()) > -1:
                            continue
                    except:
                        all_paths.append(addoutput_path)  
                        temp_paths.append(addoutput_path.lower())              
    #分组
    for path in all_paths:
        if path.find(style_online_wks[0]) > -1:
            commit_arr[0].append(path)
        elif path.find(style_online_wks[1]) > -1:
            commit_arr[1].append(path)
        elif path.find(style_online_wks[2]) > -1:
            commit_arr[2].append(path)
    
    return_content = " "
    for index in range(0,len(commit_arr)):
        print(commit_arr[index])
        print("\n\n")
        if len(commit_arr[index]) > 0:
            pywincmds.py_write_svn_message_to_file(os.linesep.join(commit_arr[index]), workspace + os.sep + "changelist.txt")    
            return_content += pysvn.commit_targets(style_online_wks[index], workspace + os.sep + "changelist.txt", style_online_username, style_online_password, content, False)
    
    #发送邮件，确认已提交
    pyemail.send(["scm@5173.com"], content.strip() + "样式已提交", return_content, [])
    pass

if phase == "update":
    update_3()
elif phase == "commit":
    commit()