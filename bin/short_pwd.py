#!/usr/bin/python

# Abbreviates printed present working directory when very long.
# Uses  ~  as  appropraite,  but  use  of  $(pwd)  use  of  soft  link
#  directories.
import os
from socket import gethostname
hostname = gethostname()
username = os.environ['USER']
pwd = os.getcwd()
homedir = os.path.expanduser('~')
pwd = pwd.replace(homedir, '~', 1)
if len(pwd) > 30:
    pwd = pwd[:10]+'...'+pwd[-20:] # first 10 chars+last 20 chars
print('[%s[@here]:%s/]$ ' % (username,
                             #hostname,
                             pwd))
