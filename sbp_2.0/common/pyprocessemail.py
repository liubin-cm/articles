'''
Created on 2012-3-14

@author: 301645
'''
from common.pyemail import pyemail

class pyprocessemail(object):
    def __init__(self):
        pass
    
    @staticmethod
    def build_success(site, to_list, sourcecode_url, sourcecode_revision, updated_content, log_url):
        '''
       parameters数组，内容是sourcecode_url, sourcecode_revision, updated_content, log_url
        '''
        title = site + "构建通过，请查看详情"
        content = '''
源代码URL：${1}

版本号：${2}
 
与线上版本比较，更新内容如下:
${3}

详细日志查询：${4}
'''
        content = content.replace('${1}', sourcecode_url).replace('${2}', sourcecode_revision).replace('${3}', updated_content).replace('${4}', log_url)
        pyemail.send(to_list, title, content, [])
        
    @staticmethod
    def commit_to_product(site, to_list, commited_content, product_test_url, product_test_message, log_url):
        title = site + "已提交产品库成功，请测试线下环境"
        content = '''
提交内容：
${1}

线下产品库地址：${2}

svn日志信息：
${3}

详细日志查询：${4}
'''
        content = content.replace('${1}', commited_content).replace('${2}', product_test_url).replace('${3}', product_test_message).replace('${4}', log_url)
        pyemail.send(to_list, title, content, [])
        
    @staticmethod
    def update_to_three(site, to_list, product_test_url, product_test_revision, updated_content, log_url):
        title = site + "三段更新成功，请测试"
        content = '''
线下产品库地址：${1}

线下产品库版本号为：${2}

三段更新详细内容如下:
${3}

详细日志查询：${4}
'''
        content = content.replace('${1}', product_test_url).replace('${2}', product_test_revision).replace('${3}', updated_content).replace('${4}', log_url)
        pyemail.send(to_list, title, content, [])
        
    @staticmethod
    def commit_to_online(site, to_list, updated_content, product_release_revision, product_release_message, log_url, release_notes_path=[]):
        #其中release_notes_path为版本说明路径,必须为列表路径，如[r"c:\版本说明"]
        title = site + "三段测试通过，请更新线上"
        content = '''
提交内容为：
${1}

svn日志信息为：
${3}

详细日志查询：${4}
'''
        content = content.replace('${1}', updated_content).replace('${2}', product_release_revision).replace('${3}', product_release_message).replace('${4}', log_url)
        pyemail.send(to_list, title, content, release_notes_path)

if __name__ == '__main__':        
    pyprocessemail.build_success('51tao', "liubin@5173.com", "http", '32', "content", "url")
    pyprocessemail.update_to_three('site', "liubin@5173.com", 'product_test_url', 'product_test_revision', 'updated_content', 'log_url')
    pyprocessemail.commit_to_product('trading', "liubin@5173.com", 'commited_content', 'product_test_url', 'product_test_message', 'log_url')
    pyprocessemail.commit_to_online('mall', "liubin@5173.com", 'updated_content', 'product_release_revision', 'product_release_message', 'hudson', [r'E:\dirs.txt'])
