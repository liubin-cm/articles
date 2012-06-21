'''
Created on 2012-3-14

@author: 301645
'''
import sys
import os
import re
import importlib
#from sites.sites_pybuild import sites_pybuild

if len(sys.argv) != 2:
    print("输入参数个数错误，请重新输入!")
    exit(1)
  
workspace = os.getenv("WORKSPACE", r"D:\Documents and Settings\binliu\workspace")
site = sys.argv[1]
#site = "test"
copiled_pattern = re.compile(".*_update.py", re.I)
files = os.listdir(workspace + r"\sbp_2.0\sites" + os.sep + site)
print(workspace + r"\sbp_2.0\sites" + os.sep + site)
build_module = ""
for file_name in files:
    mat = re.search(copiled_pattern, file_name)
    if mat:
        build_module = file_name
        break

if build_module != "":
    build_module = "sites." + site + "." + build_module.split(".")[0].strip()
    pass
else:
    build_module = "sites.sites_pyupdate"
    pass
m = importlib.import_module(build_module)
build_class = getattr(m, build_module.split(".")[-1])
print(m)
print(build_class)
p = build_class(site)

if __name__ == "__main__":
    if os.getenv("phase") == "update_3":
        p.update(True)
    elif os.getenv("phase") == "update_3_without_recycling_apppool":
        p.update(False)
    elif os.getenv("phase") == "revert":
        p.revert()
    elif os.getenv("phase") == "commit":
        p.commit()
    elif os.getenv("phase") == "resend_update_email":
        p.resend_email()
    elif os.getenv("phase") == "make_label":
        p.make_label()


#import_string = "import sites.sites_pybuild"
#exec(import_string)
#print(dir("sites.sites_pybuild"))
#p = sites_pybuild("test")
#amod = sys.modules["sites_pybuild"]
#print(sys.modules)

#m1 = importlib.import_module("sites.sites_pybuild")
#print(m1)
#m = __import__("sites.sites_pybuild", level = 0)
#m1=__import__("sites_pybuild")
#print(m)
#aclass = getattr(m1, "sites_pybuild")
#print(m1)
#aclass1 = getattr(aclass, "sites_pybuild")
#print(aclass)
#print(aclass1)
#p = aclass("test")