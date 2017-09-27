#!/usr/bin/env python

import os
import sys
import linecache

import logging

import signal
import functools

def init_log():
    logger = logging.getLogger("mylogger")
    loghdlr = logging.StreamHandler()
    fmt = logging.Formatter("[%(asctime)s] [%(levelname)s] %(module)s %(lineno)d %(message)s")
    loghdlr.setFormatter(fmt)
    logger.addHandler(loghdlr)
    logger.setLevel(logging.DEBUG)

def _log(*args):
    
    
    logger = logging.getLogger("mylogger")
    _log_severity={}
    _log_severity["DEBUG"] = logger.debug
    _log_severity["INFO"] = logger.info
    _log_severity["WARN"] = logger.warning
    _log_severity["ERROR"] = logger.error
    _log_severity["CRITICAL"] = logger.critical
    
#     print _log_severity
    
    if len(args) == 1:
        _severity = "DEBUG"
        _msg = args[0]
    elif len(args) == 2:
        _severity = args[0]
        _msg = args[1]
    
    _log_severity[_severity](_msg)
        

'''
    decorator @trace
'''
def trace(f):
    def localtrace(frame, event, arg):
        if 'line' == event:
            filepath = frame.f_code.co_filename
            lineno = frame.f_lineno
#             print 'filepath =', frame.f_code
            print '{filepath}({lineno}):{line}'.format(
                filepath=filepath,
                lineno=lineno,
                line=linecache.getline(filepath, lineno).strip('\r\n'))
            
            return localtrace
        
    def globaltrace(frame, event, arg):
        if 'call' == event:
            print 'call'
            return localtrace
              
#         return None

    def _f(*arg, **kwards):
        sys.settrace(globaltrace)
        result = f(*arg, **kwards)
        sys.settrace(None)
        return result
    
    return _f



class TimeoutError(Exception):
    pass

def timeout(seconds, error_message='Function call timed out'):
    def decorated(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)

            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)

            return result
        return functools.wraps(func)(wrapper)
    return decorated


@timeout(3)
def slowfunc(sleep_time):
    import time
    time.sleep(sleep_time)

@trace
def xxx():
    print 1

    result = ''
    for i in ['1', '2', '3']:
        if i == '3':
            result += i

    print result

if '__main__' == __name__:
#     xxx()
    slowfunc(1)
    print 'ok'
    
    try:
        slowfunc(5)
    except TimeoutError:
        print 'timeout'








    