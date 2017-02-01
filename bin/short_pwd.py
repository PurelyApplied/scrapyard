import os
from socket import gethostname
hostname = gethostname()
username = os.environ['USER']
prefix_length = 30
try:
    pwd = os.getcwd()
except:
    pwd = "a/deleted/dir?"
homedir = os.path.expanduser('~')
pwd = pwd.replace(homedir, '~', 1)
if len(pwd) > prefix_length:
    pwd = pwd[:10]+'...'+pwd[-(prefix_length - 10):]
print('[%s[@here]:%s/]$ ' % (username,
                             #hostname,
                             pwd))
