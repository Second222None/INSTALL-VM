#!/usr/bin/env python

'''
    author: weisong
    date:   2017.10.10
    usage: python virtauto.py --config file.csv
'''

import os
import sys
import re
import string
from optparse import OptionParser
from lib.config import parse_config
from lib.cli import TKCLI

# mycwd=os.getcwd()
# modcwd=mycwd+'/virtmod'
# sys.path.append(modcwd)

from lib.virtmod import colpt
from lib import classvm
from lib.virtmod import syncTemp

import logging
from lib.code_assistance import init_log
# from turtle import config_dict
# from collections import Counter
global vmurl1,vmurl2,urlcount

vmurl1 = 'http://10.10.26.90/'
# vmurl1="ftp://virtftp:1qa2ws3ed4rF@211.147.0.120:38602/"
# vmurl2="ftp://virtftp:1qa2ws3ed4rF@116.211.20.200:38602/"
urlcount=0

logger = logging.getLogger("mylogger")

def option():
    
    _path = re.compile(".*\/").search(os.path.realpath(__file__)).group(0)
    
    usage =  'usage: %prog [options] [command]'
    _parser = OptionParser(usage)
    
    _parser.add_option("--config-file", \
                       dest="conf", \
                       default= _path + "config/vm.csv", \
                       help="The location of the config file directory")
    
    _parser.add_option("--url", \
                       dest="url", \
                       default= _path + "http://10.10.26.90", \
                       help="Give path to download vm images")
    
    
    _parser.set_defaults()
    (options, _args) = _parser.parse_args()
    
    return options

def vm_ct(options):
    ''' 
        split vm info and assign to vm object
        and create vm inst
    '''
    j = 0
    
#     config_dict = parse_config("vm.csv")
    config_dict = parse_config(options.conf)
    logger.debug(config_dict)
    vminicouter =  len(config_dict)
    logger.debug('The number of vm is ' + str(vminicouter))
    
    print "vm config info is:"
    while j < vminicouter:
        
        colpt.ptred("vm " + str(j) + " info")
        colpt.ptyellow(str(config_dict['VM'+str(j+1)]))
        
        vmtmp=classvm.vm()
        ifvg = config_dict['VM'+str(j+1)]['DISK_PATTERN']
        logger.debug(ifvg)
        if(ifvg.find('lvm')>0):
            vmtmp.vgname = 'lvm'
        elif(ifvg.find('cponly')>0):
            vmtmp.vgname='none'
        
            
        vmtmp.temp = config_dict['VM'+str(j+1)]['IMAGE_NAME']
        logger.debug(vmtmp.temp)
        
        c=syncTemp.checkTempFile(vmtmp.temp,vmurl1,vmurl1)
        print str(c)+" is check vm iamges error status"
        
        if(c != 0):
            colpt.ptred('vm images erros Please check!!!')
            sys.exit(5)
        colpt.ptgreen('vm images check is ok!')
        
        vmtmp.name = config_dict['VM'+str(j+1)]['VM_NAME']
        vmtmp.define_vda_vdb()
        vmtmp.pwd = config_dict['VM'+str(j+1)]['PASSWORD']
        vmtmp.disk1_size = config_dict['VM'+str(j+1)]['DISK1']
        vmtmp.disk2_size = config_dict['VM'+str(j+1)]['DISK2']
        vmtmp.mem = config_dict['VM'+str(j+1)]['MEMORY']
        vmtmp.cpu = config_dict['VM'+str(j+1)]['VCPU_NUM']
        vmtmp.out_type = config_dict['VM'+str(j+1)]['NIC_VIRT']
        vmtmp.out_bridge = config_dict['VM'+str(j+1)]['NIC1_BRIDGE']
        vmtmp.in_bridge = config_dict['VM'+str(j+1)]['NIC2_BRIDGE']
        vmtmp.vnc_port = config_dict['VM'+str(j+1)]['VNC_PORT']
        vmtmp.outip = config_dict['VM'+str(j+1)]['NIC1_IP']
        vmtmp.outmask = config_dict['VM'+str(j+1)]['NIC1_NETMASK']
        vmtmp.outgw = config_dict['VM'+str(j+1)]['NIC1_GATEWAY']
        vmtmp.in_type = config_dict['VM'+str(j+1)]['NIC_VIRT']
        vmtmp.inip = config_dict['VM'+str(j+1)]['NIC2_IP']
        vmtmp.inmask = config_dict['VM'+str(j+1)]['NIC2_NETMASK']
        vmtmp.ingw = config_dict['VM'+str(j+1)]['NIC2_GATEWAY']
        
        if vmtmp.vm_xmlfile_exist() == '1':
            colpt.ptred('xml or vda vdb file exist skip vm create!')
        elif vmtmp.vm_host_exist() == '1':
            colpt.ptred('vm already exist skip vm create!')
        else:
            vmtmp.vm_os_check()
#             vmtmp.vm_cp_disk1()
            
            if vmtmp.vgname == 'none':
                vmtmp.vm_resize_disk1()
                vmtmp.vm_resize_disk2()
            elif vmtmp.vgname == 'lvm':
                logger.debug('undefine')
                exit()
            
            vmtmp.vm_xmlfile_create2()
            vmtmp.vm_nicinfo_copy_in()
            
            if vmtmp.pwd == 'none':
                pass
            else:
                vmtmp.vm_set_passwd()
            
            if vmtmp.vm_define() == '1':
                colpt.ptred('define failed skip vm create!')
            else:
                vmtmp.vm_run()
                vmtmp.vm_autostart()
            
            
        j = j + 1
        
    
            
if "__main__" == __name__:
    
    init_log() 
    options = option() 
    vm_ct(options)
    colpt.ptgreen('Done')

    
    
