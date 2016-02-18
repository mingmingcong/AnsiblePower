from __future__ import unicode_literals
from django.db import models
from django import forms


# Create your models here.

class AnsibleGroup(models.Model):
    group_name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ansible_group'
        verbose_name = 'group'
        verbose_name_plural = 'group'

    def __unicode__(self):
        return unicode(self.group_name)


class AnsibleHost(models.Model):
    hostname = models.CharField(max_length=45, blank=True, null=True)
    ip = models.CharField(max_length=45, blank=True, null=True,verbose_name='IP')
    username = models.CharField(max_length=45, blank=True, null=True,help_text='You must copy Public key to remote host before adding this host.')
    ansible_group = models.ForeignKey(AnsibleGroup, models.DO_NOTHING, verbose_name='group')

    class Meta:
        managed = False
        db_table = 'ansible_host'
        verbose_name = 'host'
        verbose_name_plural = 'host'

    def __unicode__(self):
        return ''




class AnsibleVariable(models.Model):
    variable_key = models.CharField(max_length=100, blank=True, null=True)
    variable_value = models.CharField(max_length=100, blank=True, null=True)
    ansible_group = models.ForeignKey(AnsibleGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ansible_variable'

    def __unicode__(self):
        return ''
