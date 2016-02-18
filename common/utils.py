# coding=utf-8
import yaml
import os
import random
import datetime
import signal
import subprocess
import time
import base64
from Crypto.Cipher import AES
from ansible import constants as C
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play_context import PlayContext
from ansible.utils.vars import load_extra_vars
from ansible.vars import VariableManager
from string import join
from django.utils import timezone

basedir = os.path.dirname(os.path.abspath(__file__))


def playbook_random_path():
    """
    generate a random playbook path
    :return: playbook absolute path
    """
    tmp_pb_name = "%s%s%s.yml" % (
        datetime.datetime.now().__hash__(), random.randint(0, 99999999),
        datetime.datetime.strftime(timezone.now(), '-%d'))
    return os.path.join(basedir, 'playbook_templates', tmp_pb_name)


def inventory_random_path():
    tmp_inventory_name = "%s%s%s" % (
        datetime.datetime.now().__hash__(), random.randint(0, 99999999),
        datetime.datetime.strftime(timezone.now(), '-%d'))
    return os.path.join(basedir, 'inventory_temp', tmp_inventory_name)


def playbook_module_replace(module_name):
    """
    specify a module name in adhoc.yml
    :param module_name:
    :return: absolute playbook path
    """
    pb_path = os.path.join(basedir, 'playbook_templates', 'adhoc.yml')
    with file(pb_path) as f:
        pb = yaml.load(f)
        task = pb[0]['tasks'][0]
        module_args_tplt = task.get('module_name')
        task[module_name] = module_args_tplt
        del task['module_name']

    tmp_pb_path = playbook_random_path()
    with file(tmp_pb_path, 'w') as f:
        yaml.dump(pb, f)
    return tmp_pb_path


def playbook_generate_yaml(playbook_model):
    """
    transfer a model to yml file
    :param playbook_model:
    :return: absolute playbook path
    """
    pb_text = [
        dict(
            hosts='{{hosts}}',
            name='{{task_id}}:{{instance_type}}',
            tasks=[{'name': str(task.task_name), str(task.ansible_module.module_name): str(task.module_args),
                    'ignore_errors': True if task.ignore_errors else False,
                    'notify': str(task.task_notify).split(',')} for task in playbook_model.ansibleplaybooktask_set.all()
                   ],
            handlers=[
                {'name': str(handler.handler_name), str(handler.ansible_module.module_name): str(handler.module_args)}
                for handler in playbook_model.ansibleplaybookhandler_set.all()
                ]
        )]

    if playbook_model.playbook_path:
        pb_path = playbook_model.playbook_path
    else:
        pb_path = playbook_random_path()
    with file(pb_path, 'w') as f:
        yaml.dump(pb_text, f)

    return pb_path


def playbook_list_hosts(pattern, host_list=C.DEFAULT_HOST_LIST):
    loader = DataLoader()
    variable_manager = VariableManager()
    inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=host_list)
    return inventory.get_hosts(pattern)


# def playbook_syntax_check(playbook_path):
#     if os.path.exists(playbook_path):
#         res = local_cmd('ansible-playbook --syntax-check  %s' % playbook_path)
#         print res

def model_to_inventory(group_queryset):
    lines = []
    for group in group_queryset:
        lines.append('\n[%s]\n' % group.group_name)
        for host in group.ansiblehost_set.all():
            lines.append('%s ansible_user=%s\n' % (host.ip, host.username))

    inventory_path = inventory_random_path()
    with file(inventory_path, 'w') as f:
        f.writelines(''.join(lines))
    return inventory_path


def local_cmd(cmd, timeout=1200):
    """call shell-command and either return its output or kill it
    if it doesn't normally exit within timeout seconds and return None
    """
    start = datetime.datetime.now()

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while process.poll() is None:
        time.sleep(0.2)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG);
            return None, None
    return process.stderr.read()


class Encryptor(object):
    AES_KEY = '452741f662c2d5e1'

    @staticmethod
    def encrypt(text):
        """
        AES加密，文本必须要16的倍数，不是则补足。
        :return:
        """
        key = Encryptor.AES_KEY
        cryptor = AES.new(key, AES.MODE_ECB)

        length = 16
        count = len(text)
        add = length - (count % length)
        text += ('\0' * add)
        ciphertext = base64.encodestring(cryptor.encrypt(text))
        return join(ciphertext.split('\n'), '')

    @staticmethod
    def decrypt(text):
        """
        解码时去掉末尾空格
        """
        key = Encryptor.AES_KEY
        cryptor = AES.new(key, AES.MODE_ECB)
        plain_text = cryptor.decrypt(base64.decodestring(text))
        return plain_text.rstrip('\0')


if __name__ == '__main__':
    print Encryptor.encrypt("dwdwdwdwdwdw").strip()

    print Encryptor.decrypt('XZw8HI7xehxHT4VhHJiOMQ==')
