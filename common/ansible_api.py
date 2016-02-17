import os
import signal
import subprocess
import time
import simplejson
from datetime import datetime
from string import join
from common.utils import local_cmd

basedir = os.path.dirname(os.path.abspath(__file__))


class AnsibleApi():
    def __init__(self, playbook_path, **kwargs):
        inventory_path = kwargs.get('inventory_path','')
        self.ansible_args = join([playbook_path, "-e", """'%s'"""%simplejson.dumps(kwargs),'-i',inventory_path], ' ')

    def run(self):
        local_cmd("ansible-playbook %s" % self.ansible_args)


if __name__ == '__main__':
    pass
    # kwargs = dict(
    #     hosts='all',
    #     table_name='ddsds',
    #     task_id='dsdsdsds',
    #     module_args='nginx -t'
    # )
    # cli = AnsibleApi(os.path.join(basedir, 'playbooks', '65259223208672901869978181.yml'), **kwargs)
    # cli.run()
