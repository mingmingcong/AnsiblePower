from __future__ import unicode_literals
from django.db import models
from common.utils import playbook_generate_yaml


# Create your models here.
class AnsibleModule(models.Model):
    module_name = models.CharField(unique=True, max_length=45)
    module_describe = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ansible_module'
        verbose_name_plural = 'modules'
        verbose_name = 'module'

    def __unicode__(self):
        return unicode(self.module_name)


class AnsiblePlaybook(models.Model):
    playbook_name = models.CharField(unique=True, max_length=45, blank=True, null=True, verbose_name='name')
    playbook_hosts = models.CharField(max_length=45, blank=True, null=True, verbose_name='hosts',default="'{{hosts}}'")
    playbook_path = models.CharField(max_length=200, blank=True, null=True, verbose_name='playbook_path')
    class Meta:
        managed = False
        db_table = 'ansible_playbook'
        verbose_name = 'playbook'






class AnsiblePlaybookHandler(models.Model):
    handler_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='handler')
    module_args = models.CharField(max_length=200, blank=True, null=True)
    ansible_module = models.ForeignKey(AnsibleModule, models.DO_NOTHING, verbose_name='module')
    ansible_playbook = models.ForeignKey(AnsiblePlaybook, models.CASCADE)

    class Meta:
        managed = False
        db_table = 'ansible_playbook_handler'
        verbose_name = 'handler'

    def __unicode__(self):
        return unicode('')


class AnsiblePlaybookTask(models.Model):
    task_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='task')
    task_notify = models.CharField(max_length=45, blank=True, verbose_name='notify',default='')
    module_args = models.CharField(max_length=200, blank=True, null=True)
    ansible_module = models.ForeignKey(AnsibleModule, models.DO_NOTHING, verbose_name='module')
    ansible_playbook = models.ForeignKey(AnsiblePlaybook, models.CASCADE)
    ignore_errors = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'ansible_playbook_task'
        verbose_name = 'task'

    def __unicode__(self):
        return unicode('')
