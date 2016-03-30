import logging

from mock import Mock
from slippinj.cli.ssh import SSHClient

import pytest


class TestSSHClient:
    def test_path_where_private_keys_files_are_stored_can_be_got(self):
        ssh_client = SSHClient(Mock(), self.__generate_test_logger(), '/test')

        assert '/test/unit.pem' == ssh_client.get_pem_path('unit')

    def test_command_can_be_executed_succesfully(self):
        ssh_lib_mocked = Mock()
        ssh_lib_mocked.connect = Mock(return_value=True)
        ssh_lib_mocked.exec_command = Mock(return_value=('test', ['test'], ''))
        ssh_lib_mocked.close = Mock(return_value=True)

        assert 'test ' == SSHClient(ssh_lib_mocked, self.__generate_test_logger()).exec_command('ls', 'unit', 'test')

    def test_command_fails_and_the_execution_does_not_stop(self):
        error_mocked = Mock()
        error_mocked.read = Mock(return_value='test')

        ssh_lib_mocked = Mock()
        ssh_lib_mocked.connect = Mock(return_value=True)
        ssh_lib_mocked.exec_command = Mock(return_value=('test', ['test'], error_mocked))
        ssh_lib_mocked.close = Mock(return_value=True)

        assert 'test ' == SSHClient(ssh_lib_mocked, self.__generate_test_logger()).exec_command('ls', 'unit', 'test')

    def test_command_fails_and_execution_is_stopped(self):
        error_mocked = Mock()
        error_mocked.read = Mock(return_value='test')

        ssh_lib_mocked = Mock()
        ssh_lib_mocked.connect = Mock(return_value=True)
        ssh_lib_mocked.exec_command = Mock(return_value=('test', ['test'], error_mocked))
        ssh_lib_mocked.close = Mock(return_value=True)

        with pytest.raises(RuntimeError) as runtime_error:
            SSHClient(ssh_lib_mocked, self.__generate_test_logger()).exec_command('ls', 'unit', 'test', True)

        assert 'test' == str(runtime_error.value)

    def test_open_sftp(self):
        sftp_client_mocked = Mock()

        ssh_lib_mocked = Mock()
        ssh_lib_mocked.connect = Mock(return_value=True)
        ssh_lib_mocked.open_sftp = Mock(return_value=sftp_client_mocked)

        assert sftp_client_mocked == SSHClient(ssh_lib_mocked, self.__generate_test_logger()).open_sftp('unit', 'test')

    def __generate_test_logger(self):
        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        return logger
