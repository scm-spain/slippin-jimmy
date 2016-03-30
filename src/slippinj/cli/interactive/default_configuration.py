from injector import inject, AssistedBuilder
from slippinj.cli.deploy_configuration import DeployConfiguration


class DefaultConfiguration(object):
    """Get the default configuration for the workflows"""

    @inject(deploy_configuration=AssistedBuilder(DeployConfiguration), configuration_parser='configuration_parser')
    def __init__(self, deploy_configuration, configuration_parser):
        """
        Initialize the class
        :param deploy_configuration: DeployConfiguration
        :param configuration_parser: ConfigParser
        """
        super(DefaultConfiguration, self).__init__()

        self.__deploy_configuration = deploy_configuration
        self.__configuration_parser = configuration_parser

    def get(self, environment, arguments, workflow_configuration):
        """
        Get configuration parameters that are common to the workflows
        :param environment: string
        :param arguments: Namespace
        :param workflow_configuration: dict
        :return: dict
        """
        default_variables = ['hive_metastore_bucket', 'hdfs_deploy_folder']
        default_configuration = {}
        interactive_provided = False
        deploy_configuration = self.__deploy_configuration.build(environment=environment,
                                                                 configuration_parser=self.__configuration_parser)
        args = vars(arguments)

        for variable in default_variables:
            if variable in args and False != args[variable]:
                default_configuration[variable] = args[variable]
                interactive_provided = True
            elif variable in workflow_configuration:
                default_configuration[variable] = workflow_configuration[variable]
            elif deploy_configuration.get(variable):
                default_configuration[variable] = deploy_configuration.get(variable)
            else:
                default_configuration[variable] = raw_input(
                    'Please, provide the {var_name} value: '.format(var_name=variable.replace('-', ' ')))
                interactive_provided = True

        if interactive_provided and 'y' == (
                raw_input('Would you like to save the provided information in the config file: [Y/N] ')).lower():
            for key in default_configuration:
                deploy_configuration.set(key, default_configuration[key])

        return default_configuration
