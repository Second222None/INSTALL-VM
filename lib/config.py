#!/usr/bin/env python

import re
import os
import logging
from code_assistance import init_log

logger = logging.getLogger("mylogger")

def parse_config(config_file, *awk):
    
    _config_dict = {}
    _lines = []
    
#     path = re.compile(".*\/").search(os.path.realpath(__file__)).group(0) + "../"
#     _config_file = path + "config/" + config_file

    if os.path.isfile(config_file):
        logger.debug("Configuration file exist")
        
        fh = open(config_file, 'r')
        _config_lines = fh.read()
        fh.close()
        
        _config_lines = _config_lines.split("\n")
        
        for _line in _config_lines:
            comment = re.compile("(#.*)").search(_line)
            if comment is not None:
                _line = _line.replace(comment.group(0), "").strip()
            else:
                _lines.append(_line)
    
    print _lines
    
    for _line in _lines:
        _line = _line.strip()
        if len(_line) == 0 :
            continue
        if _line[0].count('[') :
            _curr_global_object = _line.strip()
            _curr_global_object = _curr_global_object[1:-1]
            if _curr_global_object not in _config_dict:
                _config_dict[_curr_global_object] = {}
        elif len(_line) > 1 :
            _tmp = _line.split('=')
            if len(_tmp) < 2 :
                raise Exception("configuration error: " + _line)
                exit(1)
            _key = _tmp[0].strip()
            _value = _tmp[1].strip()
#             logger.debug("global_section = " + _curr_global_object + ", key = " + _key + ", value = " + _value)
            _config_dict[_curr_global_object][_key] = _value
    
    return _config_dict
        
    
if "__main__" == __name__:
    init_log()
    
    config_dict = parse_config("vm.csv")
     
    print config_dict    

