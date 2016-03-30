import logging

from mock import Mock

from slippinj.filesystem.yaml_configuration import YamlConfiguration, WorkflowsYamlConfigurationWriter


class TestYamlConfiguration:
    def setup_method(self, method):
        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        self.yaml = YamlConfiguration(logger)

    def teardown_method(self, method):
        self.yaml = False

    def test_yaml_can_be_read(self, tmpdir):
        c = tmpdir.mkdir('config').join('config.yml')
        c.write('content: test')

        assert {'content': 'test'} == self.yaml.read_config_file(str(c.realpath()))

    def test_yaml_with_include_can_be_read(self, tmpdir):
        config_dir = tmpdir.mkdir('config')

        c1 = config_dir.join('config1.yml')
        c1.write('content: !include config2.yml')

        c2 = config_dir.join('config2.yml')
        c2.write('content2: test2')

        configuration = self.yaml.read_config_file(str(c1.realpath()))

        assert {'content': {'content2': 'test2'}} == configuration

    def test_multiple_yaml_can_be_read(self, tmpdir):
        config_dir = tmpdir.mkdir('config')

        c1 = config_dir.join('config1.yml')
        c1.write('content: test')

        c2 = config_dir.join('config2.yml')
        c2.write('content2: test2')

        configuration = self.yaml.read_multiple_config_files([str(c1.realpath()), str(c2.realpath())])

        assert {'content': 'test', 'content2': 'test2'} == configuration


class TestWorkflowsYamlConfigurationWriter:
    def test_generate_yaml_files_providing_db_password(self):
        logger = logging.getLogger('test')
        logger.addHandler(logging.NullHandler())

        mocked_filesystem = Mock()
        mocked_filesystem.write_file = Mock(return_value=True)

        mocked_tables_configuration = Mock()
        mocked_tables_configuration.generate_configuration = Mock(return_value={})

        WorkflowsYamlConfigurationWriter(mocked_filesystem, mocked_tables_configuration, logger).generate_yaml_files(
            Mock(), {},
            'test_driver',
            'test_host',
            'test_port',
            'test_user',
            'test_db_name',
            'test_password')

        assert 2 == mocked_filesystem.write_file.call_count
        assert mocked_tables_configuration.generate_configuration.called
