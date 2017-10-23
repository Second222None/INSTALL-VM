#!/usr/bin/env python

'''
    author: weisong
    date:   2017.10.10
    usage: python virtauto.py --config file.csv
'''

import os
import sys
import string
import getopt
from lib.config import parse_config

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


global vminicouter
global vg
global vmurl1,vmurl2,urlcount
vg="vmVG"          #defaulf vg name
vg="datavg"
vmurl1 = 'http://10.10.26.90'
# vmurl1="ftp://virtftp:1qa2ws3ed4rF@211.147.0.120:38602/"
# vmurl2="ftp://virtftp:1qa2ws3ed4rF@116.211.20.200:38602/"
urlcount=0

logger = logging.getLogger("mylogger")

def getopts():
    helpinfo="""
    -h, --help print this
    --vg,assige vg name,such as --vg=datavg,vg=vmVG
        default vg name is 'datavg' if not assige
    --config,assige config file name ,such as --config=vm.csv
        config file must in same directory and must be csv
        default config file name is 'vm.csv' if not assige
    --url,give path to download vm images,such as --url=ftp://user1:pass@172.16.1.100/
    """
    global vg
    opts,args=getopt.getopt(sys.argv[1:],"hc:",["vg=","config=","help","url="])
    if opts==[]:
        colpt.ptgreen(helpinfo)
        colpt.ptgreen("Will run in default!")
    for o,a in opts:
        if o in ("-h","--help"):
            colpt.ptgreen(helpinfo)
            sys.exit(12)
        elif o=="--vg":
            vg=a
            b="vg name is "+a
            colpt.ptgreen(b)
        elif o=="--config":
            pass
        elif o=="--url":
            vmurl=a
            b="url is "+a
            colpt.ptgreen(b)
        else:
            print "wrong argument ,pleale check again"
            sys.exit(11)
            assert False,"unhand option"
 

def vm_ct():
    ''' 
        split vm info and assign to vm object
        and create vm inst
    '''
    global vg
    j = 0
    
    config_dict = parse_config("vm.csv")
    logger.debug(config_dict)
    vminicouter =  len(config_dict)
    logger.debug('The number of vm is ' + str(vminicouter))
    
    print "vm config info is:"
    while j < vminicouter:
        
        colpt.ptred("vm " + str(j) + " info")
        colpt.ptyellow(str(config_dict['VM'+str(j+1)]))
        
        vmtmp=classvm.vm()
        ifvg = config_dict['VM'+str(j+1)]['IMAGE_FORMAT']
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
    getopts()     
    vm_ct()
    colpt.ptgreen('Done')
