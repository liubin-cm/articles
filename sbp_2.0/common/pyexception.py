'''
Created on 2012-3-9

@author: 301645
'''

class pycmd_run_error(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

if __name__ == "__main__":
    try:
        raise pycmd_run_error(2*2)
    except pycmd_run_error as e:
        print('My exception occurred, value:', e.value)