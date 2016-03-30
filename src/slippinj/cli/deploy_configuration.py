import os.path


class DeployConfiguration(object):
    """Manage the deploy configuration file"""

    def __init__(self, environment, configuration_parser):
        """
        Initialize the class
        :param environment: string
        :param configuration_parser: ConfigParser
        """
        super(DeployConfiguration, self).__init__()
        self.__environment = environment
        self.__configuration_file_path = os.path.join(os.path.expanduser('~'), '.slippinj')
        self.__configuration_parser = configuration_parser

    def file_exists(self):
        """
        Check if configuration file is present in filesystem
        :return: boolean
        """
        return os.path.exists(self.__configuration_file_path)

    def environment_exists(self):
        """
        Check if environment configuration exists in configuration file
        :return: boolean
        """
        if self.file_exists():
            self.__configuration_parser.read(self.__configuration_file_path)

            return self.__configuration_parser.has_section(self.__environment)

        return False

    def get(self, key):
        """
        Get the given parameter from the configuration file for the current environment
        :param key: string
        :return: string
        """
        if self.file_exists() and self.environment_exists():
            self.__configuration_parser.read(self.__configuration_file_path)

            return self.__configuration_parser.get(self.__environment, key) if self.__configuration_parser.has_option(
                self.__environment, key) else False

        return False

    def set(self, key, value):
        """
        Save given key and value into given configuration file inside current environment
        :param key: string
        :param value: string
        """
        self.__configuration_parser.read(self.__configuration_file_path)

        if not self.environment_exists():
            self.__configuration_parser.add_section(self.__environment)

        self.__configuration_parser.set(self.__environment, key, value)

        self.__configuration_parser.write(open(self.__configuration_file_path, 'w'))
