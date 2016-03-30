from mock import Mock

from slippinj.cli.workflow_configuration import WorkflowConfiguration


class TestWorkflowConfiguration:
    def test_get_workflow_configuration_given_one_file(self):
        yaml_configuration_mocked = self.__get_the_yaml_configuration_class_mocked()

        assert 'test' == WorkflowConfiguration(yaml_configuration_mocked).get_workflow_configuration(
            'configuration_file')
        assert True == yaml_configuration_mocked.read_config_file.called
        assert False == yaml_configuration_mocked.read_multiple_config_files.called

    def test_get_workflow_configuration_given_multiple_files(self):
        yaml_configuration_mocked = self.__get_the_yaml_configuration_class_mocked()

        assert 'test' == WorkflowConfiguration(yaml_configuration_mocked).get_workflow_configuration(
            ['configuration_file1', 'configuration_file2'])
        assert False == yaml_configuration_mocked.read_config_file.called
        assert True == yaml_configuration_mocked.read_multiple_config_files.called

    def __get_the_yaml_configuration_class_mocked(self):
        yaml_configuration_mocked = Mock()
        yaml_configuration_mocked.read_config_file = Mock(return_value='test')
        yaml_configuration_mocked.read_multiple_config_files = Mock(return_value='test')

        return yaml_configuration_mocked
