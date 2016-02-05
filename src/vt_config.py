''' configuration routines for vectest'''

import json
import argparse

# description of all configuration parameters
config_desc = \
{
    'run-exp': ('avail', 'Specify a list of experiments to be performed.', None),
    'exp-prefix': ('VECTEST', 'Specify a prefix for all experiment names.', None),
}

default_config = {}
cmdline_config = {}
exps_config = {}

def get_cmdline_config():

    parser = argparse.ArgumentParser(description='Vectorization Test Suite')
    for pname, (pdefault, pdesc, pmap) in config_desc.items():
        parser.add_argument('--%s'%pname, dest=pname.replace('-', '_'), type=str,
        default=pdefault, help='%s (default: %s)'%(pdesc, pdefault))

    args = parser.parse_args()

    for argname, argvalue in vars(args).items():
        pname = argname.replace('_', '-')
        if config_desc[pname][2] is None:
            cmdline_config[pname] = argvalue
        else:
            cmdline_config[pname] = config_desc[pname][2][argvalue]

def configure_test():

    # default config
    for key, value in config_desc.items():
        default_config[key] = value[0]

    # read command line arguments
    cmdline_config = get_cmdline_config()

def read_json_config(expid, filepath):
    # config from json file
    try:
        with open(filepath, 'r') as f:
            json_config = json.load(f)
            exps_config[expid] = json_config
    except: pass

def get_config(cname, expid=None):
    if cname in cmdline_config:
        return cmdline_config[cname]

    if expid and expid in exps_config and cname in exps_config[expid]:
        return exps_config[expid][cname]

    if cname in default_config:
        return default_config[cname]

    raise Exception('%s can not be found in configuration.'%cname)

def set_config(cname, cvalue, expid):
    if expid:
        if expid not in exps_config:
            exps_config[expid] = {}
        exps_config[expid][cname] = cvalue
        return

    cmdline_config[cname] = cvalue


