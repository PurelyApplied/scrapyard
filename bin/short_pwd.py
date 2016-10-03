import os
from socket import gethostname
hostname = gethostname()
username = os.environ['USER']
try:
    pwd = os.getcwd()
except:
    pwd = "a/deleted/dir?"
homedir = os.path.expanduser('~')
pwd = pwd.replace(homedir, '~', 1)
if len(pwd) > 30:
    pwd = pwd[:10]+'...'+pwd[-20:] # first 10 chars+last 20 chars
print('[%s[@here]:%s/]$ ' % (username,
                             #hostname,
                             pwd))
