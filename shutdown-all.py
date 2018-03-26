#!/usr/bin/env python

from lib import RemoteCommand
import logging
from lib.code_assistance import _log
from lib.code_assistance import init_log
from lib import classvm

def shutdown(IP, username, key):
    
    rc = RemoteCommand.RemoteCommand(hostname = IP, username = username, priv_key = key)
#     rc.run_os_command("mkdir SUCCESSED", IP, 22) 
    rc.run_os_command("shutdown -P now", IP, 22) 
    
if "__main__" == __name__:
    
    init_log()
    shutdown("10.0.0.11", "root", "./KEY/key.pem")
    shutdown("10.0.0.21", "root", "./KEY/key.pem")
    shutdown("10.0.0.31", "root", "./KEY/key.pem")
    shutdown("10.0.0.32", "root", "./KEY/key.pem")
    shutdown("10.0.0.41", "root", "./KEY/key.pem")
    shutdown("10.0.0.51", "root", "./KEY/key.pem")
    shutdown("10.0.0.52", "root", "./KEY/key.pem")
    
    
    
