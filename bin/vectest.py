#!/usr/bin/env python

import sys
import os.path

SCRIPT_DIR, SCRIPT_NAME = os.path.split(os.path.realpath(__file__))
VECTEST_HOME = '%s/..'%SCRIPT_DIR

# Python version check
if sys.hexversion < 0x020700F0:
    print('ERROR: %s works with Python Version 2.7 or later.'%SCRIPT_NAME)
    sys.exit(-1)
sys.path.insert(0, '%s/src'%VECTEST_HOME)
sys.path.insert(1, '%s/packages'%VECTEST_HOME)

from vt_config import configure_test, get_config
from vt_setup import load_exps

from doit.loader import generate_tasks
from doit.doit_cmd import DoitMain
from doit.cmd_base import TaskLoader
from doit.action import CmdAction

class CustomTaskLoader(TaskLoader):
    """create test tasks on the fly based on cmd-line arguments"""
    DOIT_CONFIG = {
        'verbosity': 2,
        'dep_file': os.path.join(VECTEST_HOME, '.vectest.db'),
        'num_process': 1,
        }
        #'continue': True,

    def gentask_dummy(self):
        task = {}
        task['name'] = 'dummy_task'
        task['actions'] = ['echo "TEST OUTPUT"' ]
        return task

    def _gen_tasks(self):
        for expobj in get_config('exp-object-list'):
            yield expobj._task

    def load_tasks(self, cmd, params, args):
        """implements loader interface, return (tasks, config)"""
        return generate_tasks(get_config('exp-prefix'), self._gen_tasks()), self.DOIT_CONFIG

def main():

    configure_test()

    load_exps()

    doit_main = DoitMain(CustomTaskLoader())
    return doit_main.run(['run'])

if __name__ == "__main__":
    sys.exit(main())

