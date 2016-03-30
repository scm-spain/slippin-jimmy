class ConfigurationsArgument(object):
    """Parse the configurations argument"""

    def __init__(self):
        """
        Initialize the class
        """
        super(ConfigurationsArgument, self).__init__()
        self.__keys_to_change = [
            'configurations',
            'classification',
            'properties'
        ]

    def __key_to_capital(self, configuration_dict):
        if isinstance(configuration_dict, list):
            return [self.__key_to_capital(v) for v in configuration_dict]
        elif isinstance(configuration_dict, dict):
            return dict(
                (k.capitalize() if k.lower() in self.__keys_to_change else k, self.__key_to_capital(v)) for k, v in
                configuration_dict.iteritems())
        else:
            return configuration_dict

    def parse(self, configuration):
        """
        Parse configurations from the configuration file and return it formatted
        :param configuration: dict
        :return: dict
        """
        return {
            'Configurations': list(self.__key_to_capital(configuration))
        }
