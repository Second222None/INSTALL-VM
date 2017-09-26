#!/usr/bin/env python

import logging

def init_log():
    logger = logging.getLogger()
    loghdlr = logging.StreamHandler()
    fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(module)s %(lineno)d %(message)s")
    loghdlr.setFormatter(fmt)
    logger.addHandler(loghdlr)
    logger.setLevel(logging.DEBUG)

def _log(*args):
    
    _log_severity={}
    _log_severity["DEBUG"] = logging.debug
    _log_severity["INFO"] = logging.info
    _log_severity["WARN"] = logging.warning
    _log_severity["ERROR"] = logging.error
    _log_severity["CRITICAL"] = logging.critical
    
#     print _log_severity
    
    if len(args) == 1:
        _severity = "DEBUG"
        _msg = args[0]
    elif len(args) == 2:
        _severity = args[0]
        _msg = args[1]
    
    _log_severity[_severity](_msg)
        
    