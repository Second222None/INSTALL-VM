#!/usr/bin/env python

from lib import RemoteCommand
import logging
from lib.code_assistance import _log
from lib.code_assistance import init_log
from lib import classvm

def main():
    
    init_log()
    
    rc = RemoteCommand.RemoteCommand(hostname = "10.0.0.11", username = "root", priv_key = "~/key.pem")
    rc.run_os_command("mkdir SUCCESSED","10.0.0.11",22) 
    
if "__main__" == __name__:
#    main()
    init_log()
    vm = classvm.vm()
#     ciphertext = vm.encrypted_passwd("111111")
#     print ciphertext
#     vm.vm_os_check()
    vm.vm_set_passwd()
     
