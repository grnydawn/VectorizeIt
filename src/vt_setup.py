''' Setup Experiments'''

import sys
import os
import inspect

EXP_HOME = '%s/../experiments'%os.path.dirname(os.path.realpath(__file__))
EXP_CONF = 'exptask.py'

from vt_config import set_config, get_config

class VecExp(object):
    def set_expid(self, expid):
        self.task = {}
        self.task['name'] = expid

    def gentask(self):
        if 'actions' not in self.task:
            self.task['actions'] = ['echo "TEST EXP"' ]
        return self.task

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
                expid = os.path.relpath(root, EXP_HOME)
                expobj = cls()
                expobj.set_expid(expid)
                set_config('exp-object', expobj, expid)
                explist.append(expobj)

    set_config('exp-object-list', explist, None)
