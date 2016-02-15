from __future__ import absolute_import
import os
from celery import shared_task
from common.ansible_api import AnsibleApi

@shared_task
def run_job(pb_path,**kwargs):
    api = AnsibleApi(pb_path, **kwargs)
    api.run()