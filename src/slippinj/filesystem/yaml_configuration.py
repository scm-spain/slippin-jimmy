import glob
import os

import yaml
from injector import inject


class YamlConfiguration(object):
    """Process YAML configuration files"""

    @inject(logger='logger')
    def __init__(self, logger):
        """
        Initialize the class
        :param logger: Logging
        """
        super(YamlConfiguration, self).__init__()
        yaml.add_constructor('!include', self.__yaml_include)
        self.__logger = logger

    def __yaml_include(self, loader, node):
        file_name = os.path.join(os.path.dirname(loader.name), node.value)

        with file(file_name) as inputfile:
            return yaml.load(inputfile)

    def read_config_file(self, config_file):
        """
        Read the given configuration file
        :param config_file: string
        :return: dict
        """
        if not os.path.exists(config_file):
            raise IOError('Configuration file ' + config_file + ' not found.')

        return yaml.load(open(config_file, 'r'))

    def read_multiple_config_files(self, configuration_files):
        """
        Given multiple YAML files read all and merge there content in the given order, overriding same configuration keys
        :param configuration_files: list
        :return: dict
        """
        configuration = {}

        for config_file in configuration_files:
            configuration = dict(configuration.items() + self.read_config_file(config_file).items())

        return configuration

    def autodiscover_config_files(self, root_dir):
        """
        Find all the YAML files inside the given directory
        :param root_dir: string
        :return: list
        """
        if os.path.isdir(root_dir):
            return glob.glob(os.path.join(root_dir, '*.yml')) + glob.glob(os.path.join(root_dir, '**', '*.yml'))
        else:
            return [root_dir]


class WorkflowsYamlConfigurationWriter(object):
    """Write the YAML configuration files needed to run the workflows"""

    @inject(filesystem='filesystem', tables_configuration='tables_configuration', logger='logger')
    def __init__(self, filesystem, tables_configuration, logger):
        """
        Initialize the class
        :param filesystem: Filesystem
        :param tables_configuration: TablesConfiguration
        :param logger: Logging
        """
        super(WorkflowsYamlConfigurationWriter, self).__init__()
        self.__filesystem = filesystem
        self.__tables_configuration = tables_configuration
        self.__logger = logger

    def generate_yaml_files(self, injector, tables_information, location=None):
        """
        Given tables and database connection information generate the YAML files and save them into provided location
        :param injector: Injector
        :param tables_information: dict
        :param db_driver: string
        :param db_host: string
        :param db_port: integer
        :param db_user: string
        :param db_name: string
        :param db_password: string
        :param location: string
        """
        common_data = {
            'table_base_location': 's3://${swampBucket}/<source>/<database>.<schema>/',
            'db_connection_string': tables_information['db_connection_string'],
            'mode': 'RDB',
            'template': 'incremental'
        }

        tables_output = yaml.safe_dump(self.__tables_configuration.generate_configuration(tables_information, injector),
                                       default_flow_style=False, explicit_start=False, encoding='utf-8',
                                       allow_unicode=True, width=float("inf"))
        common_output = yaml.safe_dump(common_data, default_flow_style=False, explicit_start=False, encoding='utf-8',
                                       allow_unicode=True, width=float("inf"))

        location = os.getcwd() if None == location else location

        self.__logger.debug('Saving tables configuration YAML file into {location}'.format(location=location))
        self.__filesystem.write_file(os.path.join(location, 'tables.yml'), tables_output)
        self.__logger.debug('Saving common configuration YAML file into {location}'.format(location=location))
        self.__filesystem.write_file(os.path.join(location, 'common.yml'), common_output)
