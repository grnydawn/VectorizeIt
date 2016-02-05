''' Setup Experiments'''

import sys
import os
import inspect

EXP_HOME = '%s/../experiments'%os.path.dirname(os.path.realpath(__file__))
EXP_CONF = 'exptask.py'

from vt_config import set_config, get_config

class VecExp(object):
    def set_actions(self):
        raise Exception('Subclass should implement add_actions function.')


def load_exps():
    explist = []
    for root, dirs, files in os.walk(EXP_HOME):
        if EXP_CONF in files:
            oldpath = sys.path[:]
            sys.path.insert(0, root)
            mod = __import__(EXP_CONF[:-3])
            sys.path = oldpath
            match = lambda x: inspect.isclass(x) and x is not VecExp and issubclass(x, VecExp)
            for name, cls in inspect.getmembers(mod, match):
                expname = '%s/%s'%(os.path.relpath(root, EXP_HOME), cls.__name__)
                cls.EXPID = '%s:%s'%(get_config('exp-prefix'), expname)
            for name, cls in inspect.getmembers(mod, match):
                expname = '%s/%s'%(os.path.relpath(root, EXP_HOME), cls.__name__)
                expobj = cls()
                expobj._task = {}
                expobj._task['name'] = expname
                set_config('exp-object', expobj, cls.EXPID)
                for methodname, method in inspect.getmembers(expobj, predicate=inspect.ismethod):
                    if methodname.startswith('set_'):
                        expobj._task[methodname[4:]] = method()
                explist.append(expobj)

    set_config('exp-object-list', explist, None)
