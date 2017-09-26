#!/usr/bin/env python

'''
Created on Sep 26, 2017

@author: weisong
'''

from subprocess import PIPE,Popen

from lib.code_assistance import _log
import logging


'''
    usage:
    rc = RemoteCommand(hostname = "10.0.0.11", username = "root", \
                       priv_key = "~/key.pem")
'''
logger = logging.getLogger("mylogger")

class RemoteCommand(object):
    '''
        Remote Command
    '''
   
    
    def __init__(self, hostname = "127.0.0.1", port = "22", username = None, \
                 priv_key = None,  \
                 connection_timeout = None, osci = None):
        self.pid = "process_management"
        self.hostname = hostname
        self.port = int(port)
        self.username = username
        self.priv_key = priv_key
        self.connection_timeout = connection_timeout
        self.osci = osci
#         self.thread_pools = {}
    '''
        usage:
        run_os_command("mkdir SUCCESSED","10.0.0.11",22)
    '''
    def run_os_command(self, cmdline, override_hostname = None, port = 22):
        '''
        
        '''
        if override_hostname:
            _hostname = override_hostname
        else:
            _hostname = self.hostname
        
        if _hostname == "127.0.0.1" or _hostname == "0.0.0.0" :
            _local = True
        else :
            _local = False
            
        _port = port
   
        if _local :
            if self.username == "root" :
                _cmd = "sudo su -c \"" + cmdline + "\""
            else :    
                _cmd = cmdline
        else :
            if self.username :
                _username = " -l " + self.username + ' '
            else :
                _username = ''

            if self.priv_key :
                _priv_key = " -i " + self.priv_key + ' '
            else :
                _priv_key = ''

            if self.connection_timeout :
                _connection_timeout = " -o ConnectTimeout=" + str(self.connection_timeout) + ' '
            else :
                _connection_timeout = ''

            _cmd = "ssh "
            _cmd += " -p " + str(_port) + ' ' 
            _cmd += _priv_key 
            _cmd += _connection_timeout            
            _cmd += " -o StrictHostKeyChecking=no"
            _cmd += " -o UserKnownHostsFile=/dev/null "
            _cmd += " -o BatchMode=yes " 
            _cmd += _username
            
            _cmd += _hostname + " \"" + cmdline + "\""        
            
            _msg = "running os command: " + _cmd    
#             _log(_msg)
            logger.debug(_msg)
            
            _proc_h = Popen(_cmd, shell=True, stdout=PIPE, stderr=PIPE)
        
            if _proc_h.pid :
                _status = 0
                _result_stdout = " "
                _result_stderr = " "
        
        return _status, _result_stdout, _result_stderr
        