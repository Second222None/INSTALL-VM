#!/usr/bin/env python

from lib import RemoteCommand
import logging
from lib.code_assistance import _log
from lib.code_assistance import init_log


def main():
    
    init_log()
    
    rc = RemoteCommand.RemoteCommand(hostname = "10.0.0.11", username = "root", priv_key = "~/key.pem")
    rc.run_os_command("mkdir SUCCESSED","10.0.0.11",22) 
    
    
main()