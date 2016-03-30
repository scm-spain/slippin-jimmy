import os
from collections import namedtuple

from ansible.executor.playbook_executor import PlaybookExecutor
from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from injector import inject


class AnsibleClient(object):
    """Manage all the ansible execution requests"""

    @inject(emr_cluster='emr_cluster')
    def __init__(self, emr_cluster):
        """
        Initialize the class
        :param emr_cluster: EmrCluster
        """
        super(AnsibleClient, self).__init__()
        self.__emr_cluster = emr_cluster

    def run_playbook(self, playbook_path, cluster_id):
        """
        Run the given playbook using Ansible via API
        :param playbook_path: string
        :param cluster_id: string
        :return: string
        """
        if not os.path.exists(playbook_path):
            raise LookupError('Playbook to execute not found')

        loader = DataLoader()
        cluster_information = self.__emr_cluster.get_cluster_information(cluster_id)

        inventory = Inventory(loader=loader, variable_manager=VariableManager(),
                              host_list=',' + cluster_information['public_ip'])

        options = namedtuple('Options',
                             ['listtags', 'listtasks', 'listhosts', 'syntax', 'connection', 'module_path', 'forks',
                              'remote_user', 'private_key_file', 'ssh_common_args', 'ssh_extra_args', 'sftp_extra_args',
                              'scp_extra_args', 'become', 'become_method', 'become_user', 'verbosity', 'check'])

        options = options(listtags=False, listtasks=False, listhosts=False, syntax=False, connection='ssh',
                          module_path=None, forks=100, remote_user='hadoop',
                          private_key_file=self.__emr_cluster.get_pem_path(cluster_id), ssh_common_args=None,
                          ssh_extra_args=None, sftp_extra_args=None, scp_extra_args=None, become=True,
                          become_method='sudo', become_user='hadoop', verbosity=10, check=False)

        return PlaybookExecutor(playbooks=[playbook_path], inventory=inventory, variable_manager=VariableManager(),
                                loader=loader, options=options, passwords={}).run()
