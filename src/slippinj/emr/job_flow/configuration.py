import arguments


class JobFlowConfigurationParser(object):
    """Given a configuration dict validate it and prepares to run a job flow"""

    def __init__(self):
        """
        Initialize the class
        """
        super(JobFlowConfigurationParser, self).__init__()
        self.__mandatory_parameters = [
            'name',
            'release_label',
            'instances.ec2_key_name',
            'availability_zone',
            'instances.master',
            'instances.core',
            'tags'
        ]

    def validate(self, configuration):
        """
        Validate if the given configuration has all the mandatory parameters configured
        :param configuration: dict
        :return: boolean
        """
        for key in self.__mandatory_parameters:
            if '.' in key:
                configuration_group = configuration
                for key_part in key.split('.'):
                    if key_part not in configuration_group:
                        raise AttributeError('{key}  not found in configuration file'.format(key=key))
                    configuration_group = configuration_group[key_part]
            else:
                if key not in configuration:
                    raise AttributeError('{key}  not found in configuration file'.format(key=key))

        return True

    def __to_camel_case(self, key):
        converted = ''
        for i in key.split('_'):
            converted += i.capitalize()

        return converted

    def convert_to_arguments(self, configuration):
        """
        Convert from the configuration dict to a valid dict to send as arguments to the AWS API
        :param configuration: dict
        :return: dict
        """
        configuration_converted = {}

        for key in configuration:
            new_key = self.__to_camel_case(key)
            if arguments.parser_exists(key):
                configuration_converted.update(arguments.get_parser(key).parse(configuration[key]))
            else:
                configuration_converted[new_key] = configuration[key]

        return configuration_converted
