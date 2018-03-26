#!/usr/bin/env python

'''
Created on Otc 24, 2017

@author: weisong
'''

import re
import os
from cmd import Cmd

from code_assistance import trace
from RemoteCommand import RemoteCommand

class TKCLI(Cmd):
    def __init__(self):
        self.path = re.compile(".*\/").search(os.path.realpath(__file__)).group(0) + "/../"
        print self.path
        Cmd.__init__(self)
        self.prompt = '(WEISONG)'
        Cmd.emptyline = self.emptyline()
        self.operation = RemoteCommand()
      
    @trace   
    def do_test(self, arg):
        '''
        Test
        '''
        print "TEST"
        
        
    
    def do_quit(self, line):
        '''
        Quit
        '''
        return True
    
    def do_help(self, args):
        '''
        Help info
        '''
        if not help(args) :
            Cmd.do_help(self, args)
    
    def emptyline(self):
        '''
        TBD
        '''
#         print self.lastcmd
        return
    
           
    def do_shell(self, parameters) :
        '''
        usage shell [cmd]
        '''
#         _status, _msg, _object = self.passive_operations.execute_shell(parameters, \
#                                                                     "shell-execute")  
        print parameters
        _status, _msg, _result_stderr = self.operation.run_os_command(parameters)
        
        print(_msg)
    
    
    def setup_default_options(self) :
        '''
        Do command line parsing
        '''

        _path = re.compile(".*\/").search(os.path.realpath(__file__)).group(0)
            
        usage = '''usage: %prog [options] [command]
        '''
        self.parser = OptionParser(usage)
        
        self.parser.add_option("--oldconfig", dest = "oldconfig", action = "store_true", \
                      default = False, \
                        help = "Use the deprecated configuration format.")
    
        self.parser.set_defaults()
        (self.options, self.args) = self.parser.parse_args()
        
        
if '__main__' == __name__:
    
    _cmd_processor = TKCLI()
    _cmd_processor.cmdloop()
    
    
    
    
    
    