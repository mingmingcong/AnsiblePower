from __future__ import (absolute_import, division)
import os
import sys
import django
import datetime

__metaclass__ = type
basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('/Users/taoprogramer/Documents/workspace/AnsiblePower')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AnsiblePower.settings")
django.setup()
from adhoc.models import AnsibleAdhoc, AnsibleAdhocTask
from job.models import AnsibleJob,AnsibleJobTask
from django.utils import timezone
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    task_id = None
    instance_type = None

    def __init__(self):
        super(CallbackModule, self).__init__()

    def v2_playbook_on_play_start(self, play):
        name_item = play.get_name().split(':')
        self.task_id = int(name_item[0])
        self.instance_type = name_item[1]

    def v2_runner_on_ok(self, result):
        # print result._task,result._host
        task_name = result._task.get_name()
        if self.instance_type == 'AnsibleAdhoc':
            if task_name != "setup":
                task_id = self.task_id
                stdout = result._result.get('stdout', '')
                stderr = result._result.get('stderr', '')
                end_time = timezone.now()
                AnsibleAdhocTask.objects.filter(task_host=result._host, ansible_adhoc_id=task_id).update(
                    end_time=end_time,
                    stdout=stdout,
                    stderr=stderr,
                    failure=False,
                    finish=True)
        elif self.instance_type == 'AnsibleJob':
            if task_name != 'setup':
                job_id = self.task_id
                stdout = result._result.get('stdout', '')
                stderr = result._result.get('stderr', '')
                end_time = timezone.now()
                AnsibleJobTask.objects.filter(task_name=task_name,task_host=result._host,ansible_job_id=job_id).update(
                    end_time=end_time,
                    stdout=stdout,
                    stderr=stderr,
                    failure=False,
                    finish=True
                )

    def v2_runner_on_failed(self, result, ignore_errors=False):
        task_name = result._task.get_name()
        if self.instance_type == 'AnsibleAdhoc':
            if task_name != "setup":
                task_name = task_name.split(":")
                task_id = self.task_id
                # stdout = result._result.get('stdout', '').replace('\n', '\\n')
                # stderr = result._result.get('stderr', '').replace('\n', '\\n')
                stdout = result._result.get('stdout', '')
                stderr = result._result.get('stderr', '')
                # start_time = datetime.datetime.strptime(result._result.get('start', '').split('.')[0], '%Y-%m-%d %H:%M:%S')
                # start_time = timezone.make_aware(start_time)
                end_time = timezone.now()
                AnsibleAdhocTask.objects.filter(task_host=result._host, ansible_adhoc_id=task_id).update(
                    end_time=end_time,
                    stdout=stdout,
                    stderr=stderr,
                    failure=True,
                    finish=True)
        elif self.instance_type == 'AnsibleJob':
            if task_name != 'setup':
                job_id = self.task_id
                stdout = result._result.get('stdout', '')
                stderr = result._result.get('stderr', '')
                end_time = timezone.now()
                AnsibleJobTask.objects.filter(task_name=task_name,task_host=result._host,ansible_job_id=job_id).update(
                    end_time=end_time,
                    stdout=stdout,
                    stderr=stderr,
                    failure=True,
                    finish=True
                )


    # #
    # def v2_playbook_on_task_start(self, task, is_conditional):
    #     # print task._role
    #     task_item = task.split(':')
    #     job_task = task_item[1].strip()

    # playbook finish
    def v2_playbook_on_stats(self, stats):
        end_time = timezone.now()
        if self.instance_type == 'AnsibleAdhoc':
            AnsibleAdhoc.objects.filter(id=self.task_id).update(finish=True, end_time=end_time)
        elif self.instance_type == 'AnsibleJob':
            AnsibleJob.objects.filter(id=self.task_id).update(finish=True,end_time=end_time)
