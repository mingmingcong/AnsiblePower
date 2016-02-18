from __future__ import unicode_literals

from django.db import models
from playbook.models import AnsiblePlaybook
from ansible_auth.models import AuthUser
# Create your models here.
class AnsibleJob(models.Model):
    job_name = models.CharField(max_length=45, blank=True, null=True)
    job_pattern = models.CharField(max_length=45, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    # progress_bar = models.IntegerField(blank=True,default=0)
    finish = models.BooleanField(blank=True,default=False)
    ansible_playbook = models.ForeignKey(AnsiblePlaybook, models.DO_NOTHING)
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)


    class Meta:
        managed = False
        db_table = 'ansible_job'
        ordering = ['-start_time']


class AnsibleJobTask(models.Model):
    task_name = models.CharField(max_length=100, blank=True, null=True)
    task_host = models.CharField(max_length=100, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    finish = models.BooleanField(blank=True,default=False)
    failure = models.BooleanField(blank=True,default=False)
    stdout = models.TextField(blank=True, null=True)
    stderr = models.TextField(blank=True, null=True)
    ansible_job = models.ForeignKey(AnsibleJob, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ansible_job_task'
