from injector import inject, AssistedBuilder

from slippinj.cli.ssh import SSHClient


class EmrCluster(object):
    """Handle all EMR cluster information and configuration"""

    @inject(aws_emr_client='aws_emr_client', ssh_client=AssistedBuilder(SSHClient), args='args', logger='logger')
    def __init__(self, aws_emr_client, ssh_client, args, logger):
        """
        Initialize the class
        :param aws_emr_client: EMR.client
        :param ssh_client: paramiko.SSHClient
        :param args: Namespace
        :param logger: Logging
        """
        super(EmrCluster, self).__init__()
        self.__aws_emr_client = aws_emr_client
        self.__ssh_client = ssh_client.build(pem_files_dir=args.pem_dir)
        self.__cluster_information = {}
        self.__logger = logger

    def __get_cluster_environment(self, tags):
        for tag in tags:
            if 'environment' == tag['Key'].lower():
                return tag['Value']

        return False

    def __get_cluster(self, cluster_id):
        cluster = self.__aws_emr_client.describe_cluster(ClusterId=cluster_id)
        instances = self.__aws_emr_client.list_instances(ClusterId=cluster_id, InstanceGroupTypes=['MASTER'])

        return dict(cluster.items() + instances.items())

    def __get_master_ips(self, cluster_information):
        for instance in cluster_information['Instances']:
            if cluster_information['Cluster']['MasterPublicDnsName'] == instance['PublicDnsName']:
                return instance['PublicIpAddress'], instance['PrivateIpAddress']

    def get_cluster_information(self, cluster_id):
        """
        Get the cluster information from the AWS API
        :param cluster_id: string
        :return: dict
        """
        if not cluster_id in self.__cluster_information:
            self.__logger.debug('Getting information from AWS for cluster {cluster_id}'.format(cluster_id=cluster_id))
            cluster_information = self.__get_cluster(cluster_id)

            cluster_ips = self.__get_master_ips(cluster_information)

            self.__cluster_information[cluster_id] = {
                'public_dns': cluster_information['Cluster']['MasterPublicDnsName'],
                'public_ip': cluster_ips[0],
                'private_ip': cluster_ips[1],
                'environment': self.__get_cluster_environment(cluster_information['Cluster']['Tags']),
                'key_name': cluster_information['Cluster']['Ec2InstanceAttributes']['Ec2KeyName']
            }

        return self.__cluster_information[cluster_id]

    def exec_command(self, command, cluster_id, stop_on_error=False):
        """
        Execute given command in the master of the selected cluster
        :param command: string
        :param cluster_id: string
        :param stop_on_error: boolean
        :return: string
        """
        cluster_information = self.get_cluster_information(cluster_id)

        self.__logger.debug(
            'Executing command {command} in cluster {cluster_id}'.format(command=command, cluster_id=cluster_id))
        return self.__ssh_client.exec_command(command, cluster_information['public_dns'],
                                              cluster_information['key_name'], stop_on_error)

    def open_sftp(self, cluster_id):
        """
        Open an SFTP connection to the given cluster
        :param cluster_id: string
        :return: SFTP
        """
        cluster_information = self.get_cluster_information(cluster_id)

        self.__logger.debug('Opening SFTP connection to cluster {cluster_id}'.format(cluster_id=cluster_id))
        return self.__ssh_client.open_sftp(cluster_information['public_dns'], cluster_information['key_name'])

    def get_pem_path(self, cluster_id):
        """
        Get the path to the private key file to connect to the cluster
        :param cluster_id: string
        :return: string
        """
        cluster_information = self.get_cluster_information(cluster_id)

        return self.__ssh_client.get_pem_path(cluster_information['key_name'])
