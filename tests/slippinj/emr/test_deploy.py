from mock import Mock

from slippinj.emr.deploy import EmrDeploy


class TestEmrDeploy(object):
    def test_run_properties_file(self):
        mocked_sftp_client = Mock()
        mocked_sftp_client.put = Mock(return_value=True)

        mocked_emr_cluster = Mock()
        mocked_emr_cluster.open_sftp = Mock(return_value=mocked_sftp_client)
        mocked_emr_cluster.exec_command = Mock(return_value=True)

        assert True == EmrDeploy(mocked_emr_cluster, Mock(), Mock()).run_properties_file('test', 'test')

    def test_code_is_uploaded_succesfully(self):
        mocked_sftp_client = Mock()
        mocked_sftp_client.put = Mock(return_value=True)
        mocked_sftp_client.mkdir = Mock(return_value=True)
        mocked_sftp_client.put = Mock(return_value=True)

        mocked_emr_cluster = Mock()
        mocked_emr_cluster.open_sftp = Mock(return_value=mocked_sftp_client)
        mocked_emr_cluster.exec_command = Mock(return_value=True)

        mocked_filesystem = Mock()
        mocked_filesystem.generate_tar_file = Mock(return_value='test.tar.gz')

        mocked_hdfs = Mock()
        mocked_hdfs.rmdir = Mock(return_value=True)
        mocked_hdfs.mkdir = Mock(return_value=True)
        mocked_hdfs.put = Mock(return_value=True)

        assert True == EmrDeploy(mocked_emr_cluster, mocked_hdfs, mocked_filesystem).upload_code('test', 'test', 'test', 'test')

    def test_code_upload_fails_when_creating_remote_directory(self):
        mocked_sftp_client = Mock()
        mocked_sftp_client.put = Mock(return_value=True)
        mocked_sftp_client.mkdir = Mock()
        mocked_sftp_client.mkdir.side_effect = IOError()
        mocked_sftp_client.put = Mock(return_value=True)

        mocked_emr_cluster = Mock()
        mocked_emr_cluster.open_sftp = Mock(return_value=mocked_sftp_client)
        mocked_emr_cluster.exec_command = Mock(return_value=True)

        mocked_filesystem = Mock()
        mocked_filesystem.generate_tar_file = Mock(return_value='test.tar.gz')

        mocked_hdfs = Mock()
        mocked_hdfs.rmdir = Mock(return_value=True)
        mocked_hdfs.mkdir = Mock(return_value=True)
        mocked_hdfs.put = Mock(return_value=True)

        assert False == EmrDeploy(mocked_emr_cluster, mocked_hdfs, mocked_filesystem).upload_code('test', 'test',
                                                                                                  'test', 'test')
