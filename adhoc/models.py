from __future__ import unicode_literals
from django.db import models
from ansible_auth.models import AuthUser

# Create your models here.

class AnsibleAdhoc(models.Model):
    adhoc_name = models.CharField(max_length=45, blank=True, null=True)
    adhoc_pattern = models.CharField(max_length=200, blank=True, null=True)
    adhoc_args = models.CharField(max_length=200, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    finish = models.IntegerField(blank=True, null=True)
    ansible_module = models.ForeignKey('AnsibleModule', models.DO_NOTHING)
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        db_table = 'ansible_adhoc'
        ordering = ['-start_time']


class AnsibleAdhocTask(models.Model):
    task_host = models.CharField(max_length=45, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    finish = models.BooleanField(default=False)
    failure = models.BooleanField(default=False)
    stdout = models.TextField(blank=True, null=True)
    stderr = models.TextField(blank=True, null=True)
    ansible_adhoc = models.ForeignKey(AnsibleAdhoc, models.DO_NOTHING)

    class Meta:
        db_table = 'ansible_adhoc_task'
        unique_together = (('id', 'ansible_adhoc'),)


class AnsibleModule(models.Model):
    module_name = models.CharField(unique=True, max_length=45)
    module_describe = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        db_table = 'ansible_module'
        ordering = ['module_name']
