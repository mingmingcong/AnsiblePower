from __future__ import unicode_literals
from django.db import models


# Create your models here.

class AnsibleGroup(models.Model):
    group_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ansible_group'
        verbose_name = 'group'


class AnsibleHost(models.Model):
    hostname = models.CharField(max_length=45, blank=True, null=True)
    ip = models.CharField(max_length=45, blank=True, null=True)
    ansible_group = models.ForeignKey(AnsibleGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ansible_host'


class AnsibleVariable(models.Model):
    variable_key = models.CharField(max_length=100, blank=True, null=True)
    variable_value = models.CharField(max_length=100, blank=True, null=True)
    ansible_group = models.ForeignKey(AnsibleGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ansible_variable'
