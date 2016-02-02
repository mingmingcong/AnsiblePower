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
from django.utils import timezone
from ansible.plugins.callback import CallbackBase


class CallbackModule(CallbackBase):
    task_id = None

    def __init__(self):
        super(CallbackModule, self).__init__()

    def v2_runner_on_ok(self, result):
        # print result._task,result._host
        task_name = result._task.get_name()
        if task_name != "setup":
            task_name = task_name.split(":")
            task_id = task_name[1]
            # stdout = result._result.get('stdout', '').replace('\n', '\\n')
            # stderr = result._result.get('stderr', '').replace('\n', '\\n')

            stdout = result._result.get('stdout', '')
            stderr = result._result.get('stderr', '')
            # start_time = datetime.datetime.strptime(result._result.get('start', '').split('.')[0], '%Y-%m-%d %H:%M:%S')
            # start_time = timezone.make_aware(start_time)
            end_time = timezone.now()
            AnsibleAdhocTask.objects.filter(task_host=result._host, ansible_adhoc_id=task_id).update(end_time=end_time,
                                                                                                     stdout=stdout,
                                                                                                     stderr=stderr,
                                                                                                     failure=False,
                                                                                                     finish=True)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        task_name = result._task.get_name()
        if task_name != "setup":
            task_name = task_name.split(":")
            task_id = task_name[1]
            # stdout = result._result.get('stdout', '').replace('\n', '\\n')
            # stderr = result._result.get('stderr', '').replace('\n', '\\n')

            stdout = result._result.get('stdout', '')
            stderr = result._result.get('stderr', '')
            # start_time = datetime.datetime.strptime(result._result.get('start', '').split('.')[0], '%Y-%m-%d %H:%M:%S')
            # start_time = timezone.make_aware(start_time)
            end_time = timezone.now()
            AnsibleAdhocTask.objects.filter(task_host=result._host, ansible_adhoc_id=task_id).update(end_time=end_time,
                                                                                                     stdout=stdout,
                                                                                                     stderr=stderr,
                                                                                                     failure=True,
                                                                                                     finish=True)

    def v2_playbook_on_play_start(self, play):
        self.task_id = int(play.get_name())

    def v2_playbook_on_task_start(self, task, is_conditional):
        # print task._role
        pass

    # playbook finish
    def v2_playbook_on_stats(self, stats):
        end_time = timezone.now()
        AnsibleAdhoc.objects.filter(id=self.task_id).update(finish=True,end_time=end_time)
