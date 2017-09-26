#!/usr/bin/env python

from lib import RemoteCommand

def main():
    
    rc = RemoteCommand.RemoteCommand(hostname = "10.0.0.11", username = "root", priv_key = "~/key.pem")
    
    rc.run_os_command("mkdir SUCCESSED","10.0.0.11",22) 
    
main()