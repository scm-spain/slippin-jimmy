from injector import inject


class WorkflowConfiguration(object):
    """Read the configuration for the given workflow"""

    @inject(yaml_configuration='yaml_configuration')
    def __init__(self, yaml_configuration):
        """
        Initialize the class
        :param yaml_configuration: YamlConfiguration
        """
        super(WorkflowConfiguration, self).__init__()

        self.__yaml_configuration = yaml_configuration

    def get_workflow_configuration(self, configuration_file):
        """
        Get the workflow configuration given the file or files where it can be found
        :param configuration_file: string or list, if a list is given all the files will be read sorted as they are provided
        :return: dict
        """
        return self.__yaml_configuration.read_config_file(configuration_file) if type(
            configuration_file) == str else self.__yaml_configuration.read_multiple_config_files(configuration_file)
