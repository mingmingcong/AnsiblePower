from __future__ import absolute_import
import os
from celery import shared_task
from common.ansible_api import AnsibleApi
from common.utils import playbook_module_replace,inventory_random_path
from datetime import datetime
import os
import time
import signal
import subprocess


@shared_task
def run_adhoc(**kwargs):
    module_name = kwargs.get('module_name', '')

    pb_path = playbook_module_replace(module_name)
    api = AnsibleApi(pb_path, **kwargs)
    api.run()



