from django.test import TestCase
# Create your tests here.
from ansible.inventory import Inventory,Group
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
import os
from ConfigParser import SafeConfigParser,ConfigParser,RawConfigParser

if __name__ == '__main__':
    hosts_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'host', 'hosts')
    loader = DataLoader()
    variable_manager = VariableManager()
    inventory = Inventory(loader,variable_manager,hosts_file)
    print inventory.groups
    print inventory.list_groups()
    print inventory.add_group(Group('dwdwdw'))
    print inventory.list_groups()
    inventory.serialize()