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


def trace_nothing(aFunc):
    return aFunc
        
def trace_actual(aFunc):
    
    '''
    Trace entry, exit and exceptions.
    '''
    def loggedFunc(*args, **kwargs ):
        _log_suffix = ""
        try :
            _log_prefix = aFunc.__module__ + ".py/"  + aFunc.__class__.__name__
            _log_prefix += '.' + aFunc.__name__
        except AttributeError :
            _log_prefix = aFunc.__module__ + ".py/" + aFunc.__name__
        _msg = _log_prefix + " - Entry point " + _log_suffix
        logging.debug( _msg)
#         print _msg
        
        try:
            result = aFunc(*args, **kwargs )
        except Exception, e:
            _msg = _log_prefix + " - Exit point (Exception \"" + str(e) + "\") "
            _msg += _log_suffix
            logging.debug(_msg)
            raise
        _msg = _log_prefix + " - Exit point " + _log_suffix
        logging.debug(_msg)
#         print _msg
        return result
    loggedFunc.__name__= aFunc.__name__
    loggedFunc.__doc__= aFunc.__doc__
    
        
    return loggedFunc


'''
    decorator @trace
'''
def trace_code(f):
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

trace = trace_actual

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








    