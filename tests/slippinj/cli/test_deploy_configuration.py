import mock

from slippinj.cli.deploy_configuration import DeployConfiguration


class TestDeployConfiguration:
    def setup_method(self, method):
        self.patcher_os_path_exists = mock.patch("os.path.exists")
        self.mocked_os_path_exists = self.patcher_os_path_exists.start()

    def teardown_method(self, method):
        self.patcher_os_path_exists.stop()

    def test_file_exists(self):
        deploy_configuration = DeployConfiguration("devel", mock.Mock())

        self.mocked_os_path_exists.return_value = True

        assert True == deploy_configuration.file_exists()

    def test_file_does_not_exist(self):
        deploy_configuration = DeployConfiguration("devel", mock.Mock())

        self.mocked_os_path_exists.return_value = False

        assert False == deploy_configuration.file_exists()

    def test_environment_exists_when_config_file_is_present(self):
        mocked_config_parser = mock.Mock()
        mocked_config_parser.read = mock.Mock(return_value=True)
        mocked_config_parser.has_section = mock.Mock(return_value=True)

        self.mocked_os_path_exists.return_value = True

        deploy_configuration = DeployConfiguration("devel", mocked_config_parser)

        assert True == deploy_configuration.environment_exists()

    def test_environment_exists_when_config_file_is_not_present(self):
        mocked_config_parser = mock.Mock()
        mocked_config_parser.read = mock.Mock(return_value=True)
        mocked_config_parser.has_section = mock.Mock(return_value=True)

        self.mocked_os_path_exists.return_value = False

        deploy_configuration = DeployConfiguration("devel", mocked_config_parser)

        assert False == deploy_configuration.environment_exists()
        mocked_config_parser.read.assert_not_called()
        mocked_config_parser.has_section.assert_not_called()

    def test_environment_does_not_exist_when_config_file_is_present(self):
        mocked_config_parser = mock.Mock()
        mocked_config_parser.read = mock.Mock(return_value=True)
        mocked_config_parser.has_section = mock.Mock(return_value=False)

        self.mocked_os_path_exists.return_value = True

        deploy_configuration = DeployConfiguration("devel", mocked_config_parser)

        assert False == deploy_configuration.environment_exists()

    def test_get_variable_from_config_when_environment_and_config_file_exists(self):
        mocked_config_parser = mock.Mock()
        mocked_config_parser.read = mock.Mock(return_value=True)
        mocked_config_parser.has_section = mock.Mock(return_value=True)
        mocked_config_parser.get = mock.Mock(return_value="Test")

        self.mocked_os_path_exists.return_value = True

        deploy_configuration = DeployConfiguration("devel", mocked_config_parser)

        assert "Test" == deploy_configuration.get("testing")
        mocked_config_parser.get.assert_called_once_with("devel", "testing")

    def test_get_variable_from_config_when_environment_does_not_exist_and_config_file_exists(self):
        mocked_config_parser = mock.Mock()
        mocked_config_parser.read = mock.Mock(return_value=True)
        mocked_config_parser.has_section = mock.Mock(return_value=False)
        mocked_config_parser.get = mock.Mock(return_value="Test")

        self.mocked_os_path_exists.return_value = True

        deploy_configuration = DeployConfiguration("devel", mocked_config_parser)

        assert False == deploy_configuration.get("testing")
        mocked_config_parser.get.assert_not_called()

    def test_get_variable_from_config_when_config_file_does_not_exist(self):
        self.mocked_os_path_exists.return_value = False

        deploy_configuration = DeployConfiguration("devel", mock.Mock())

        assert False == deploy_configuration.get("testing")

    def test_set_variable_when_environment_does_not_exist(self):
        mocked_config_parser = mock.Mock()
        mocked_config_parser.read = mock.Mock(return_value=True)
        mocked_config_parser.has_section = mock.Mock(return_value=False)
        mocked_config_parser.add_section = mock.Mock(return_value=True)
        mocked_config_parser.set = mock.Mock(return_value=True)
        mocked_config_parser.write(return_value=True)

        self.mocked_os_path_exists.return_value = True

        deploy_configuration = DeployConfiguration("devel", mocked_config_parser)

        with mock.patch('__main__.open') as m:
            deploy_configuration.set("testing", "test")
            mocked_config_parser.add_section.assert_called_once_with("devel")
            assert True == mocked_config_parser.write.called

    def test_set_variable_when_environment_exists(self):
        mocked_config_parser = mock.Mock()
        mocked_config_parser.read = mock.Mock(return_value=True)
        mocked_config_parser.has_section = mock.Mock(return_value=True)
        mocked_config_parser.add_section = mock.Mock(return_value=True)
        mocked_config_parser.set = mock.Mock(return_value=True)
        mocked_config_parser.write(return_value=True)

        self.mocked_os_path_exists.return_value = True

        deploy_configuration = DeployConfiguration("devel", mocked_config_parser)

        with mock.patch('__main__.open') as m:
            deploy_configuration.set("testing", "test")
            mocked_config_parser.add_section.assert_not_called()
            assert True == mocked_config_parser.write.called
