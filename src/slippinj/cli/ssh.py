import os.path

from injector import inject


class SSHClient(object):
    """Wrapper to use the SSH client library"""

    @inject(ssh_client='ssh_lib_client', logger='logger')
    def __init__(self, ssh_client, logger, pem_files_dir=False):
        """
        Initialize the class
        :param ssh_client: paramiko.SSHClient
        :param logger: Logging
        :param pem_files_dir: string
        """
        super(SSHClient, self).__init__()
        self.__ssh_client = ssh_client
        self.__logger = logger
        self.__pem_files_dir = os.path.join(os.path.expanduser('~'),
                                           '.ssh/') if False == pem_files_dir else pem_files_dir

    def get_pem_path(self, pem_file):
        """
        Return the full path to the pem file based on the given name and configured directory where all private keys are
        :param pem_file: string
        :return: string
        """
        return os.path.join(self.__pem_files_dir, pem_file + '.pem')

    def __connect_to_cluster(self, public_dns, pem_file):
        self.__ssh_client.connect(
            public_dns,
            username='hadoop',
            key_filename=self.get_pem_path(pem_file)
        )

    def exec_command(self, command, public_dns, pem_file, stop_on_error=False):
        """
        Execute given command in a machine via SSH
        :param command: string
        :param public_dns: string
        :param pem_file: string
        :param stop_on_error: boolean
        :return: string
        """
        self.__connect_to_cluster(public_dns, pem_file)

        self.__logger.debug(
            'Executing command {command} in machine {public_dns}'.format(command=command, public_dns=public_dns))
        stdin, stdout, stderr = self.__ssh_client.exec_command(command)

        if stop_on_error:
            error = stderr.read().strip('\n')
            if error:
                raise RuntimeError(error)

        output = ''
        for line in stdout:
            output += line.strip('\n') + ' '

        self.__ssh_client.close()

        return output

    def open_sftp(self, public_dns, pem_file):
        """
        Open an SFTP connection to the given machine
        :param public_dns: string
        :param pem_file: string
        :return: SFTP
        """
        self.__connect_to_cluster(public_dns, pem_file)
        self.__logger.debug('Opening SFTP connection to {public_dns}'.format(public_dns=public_dns))
        return self.__ssh_client.open_sftp()
