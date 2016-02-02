#coding=utf-8
from django.db.models.signals import post_save
from django.dispatch import receiver
from playbook.models import AnsiblePlaybook


@receiver(post_save,sender=AnsiblePlaybook)
def playbook_to_yml(sender,**kwargs):
    """
    save playbook to a yml after save model
    :param sender:
    :param kwargs:
    :return:
    """
    pass

