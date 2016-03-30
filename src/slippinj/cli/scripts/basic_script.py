class BasicScript(object):
    def __init__(self, parser):
        """
        Initialize the class
        :param parser: ArgumentParser
        """
        super(BasicScript, self).__init__()
        self._parser = parser

    def get_arguments(self):
        """
        Get the arguments to configure current script, should be implementd in children classes
        :return: list
        """
        raise StandardError('Implement get_arguments method')

    def run(self, args, injector):
        raise StandardError('Implement run method')

    def configure(self):
        """
        Configure the component before running it
        :rtype: Class instance
        """
        self.__set_arguments()

        return self

    def __set_arguments(self):
        parser = self._parser.add_parser(self.__class__.__name__.lower(), help=self.__class__.__doc__,
                                         conflict_handler='resolve')

        arguments = self.get_arguments()

        for argument in arguments:
            short = argument['short']
            long = argument['long']
            del argument['short']
            del argument['long']
            parser.add_argument(short, long, **argument)

    def get_wf_configuration(self, args, injector):
        object_configuration = injector.get('object_configuration')

        if 1 >= len(object_configuration):
            configuration_file = args.configuration_file if 'configuration_file' in args and None != args.configuration_file else injector.get(
                'interactive_configuration_file').get(args.wf_dir)

            configuration = injector.get('wf_configuration').get_workflow_configuration(configuration_file)

            configuration = dict(
                injector.get('interactive_default_configuration').get('devel', args, configuration).items()
                + configuration.items()
            )

            for key in configuration:
                object_configuration[key] = configuration[key]

        return object_configuration
