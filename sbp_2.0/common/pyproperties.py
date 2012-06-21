'''
Created on 2012-3-12

@author: binliu
'''
import re
import yaml

class pyproperties():
    def __init__(self, config_file):
        self.config_file = config_file
        f = open(self.config_file, "r")
        try:
            self.all_config = f.read()
        except Exception as e:
            raise(e)
        finally:
            f.close()
        pass
    '''
    def get_property(self, key):
        compiled_pattern = re.compile("[\r\n]*(\s*" + key +"\s*=.*)", re.M)#re.compile("[\r\n]*(\s*" + key +"\s*=.*?)((?=\n[\w]+=)|(\n$))", re.S)
        match = re.search(compiled_pattern, self.all_config)
        if match == None:
            return(None)
        res = match.group(1).split("=" , 1)[1].strip().split(",")
        i = 0
        length = len(res)
        for i in range(0,length):
            res[i] = res[i].strip()
        if length == 1:
            return(res[0])
        return(res)
    
    #get values that match pre plus sequences
    def get_properties(self, pre):
        compiled_pattern = re.compile("[\r\n]*(" + pre + "_[\d]+):(" +".*)\s*[\r\n]*", re.M)
        all_match = re.findall(compiled_pattern, self.all_config)
        result = []
        if len(all_match) == 0:
            return(None)
        for i in all_match:
            result.append(i[1])
        return(result)
    '''
    def get_dict(self):
        return(yaml.load(self.all_config))
    
if __name__ == '__main__':  
    p = pyproperties(r"D:\Documents and Settings\binliu\workspace\sbp_2.0\sites\test\test_build.config")