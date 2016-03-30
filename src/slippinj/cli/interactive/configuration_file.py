from injector import inject


class ConfigurationFile(object):
    """Get the configuration file to use when managing workflows"""

    @inject(yaml_configuration='yaml_configuration')
    def __init__(self, yaml_configuration):
        """
        Initialize the class
        :param yaml_configuration: YamlConfiguration
        """
        super(ConfigurationFile, self).__init__()

        self.__yaml_configuration = yaml_configuration

    def get(self, wf_dir):
        """
        Ask user to select which configuration files would like to use from all the files found
        :param wf_dir: string
        :return: list
        """
        config_files_found = self.__yaml_configuration.autodiscover_config_files(wf_dir)
        if 0 == len(config_files_found):
            raise IOError('No configuration files has been found')
        elif 1 == len(config_files_found):
            config_files = config_files_found
        else:
            print 'Select the configuration files you want to process'
            for index, cf in enumerate(config_files_found):
                print '[{index}] {config_file}'.format(index=index, config_file=cf.replace(wf_dir, ''))

            selected_files = raw_input('For multiple files separate them using ",": ')
            if 1 > len(selected_files):
                raise ValueError('You must select at least one configuration file to process the workflows')

            config_files = []
            for index in selected_files.split(','):
                try:
                    config_files.append(config_files_found[int(index)])
                except ValueError:
                    pass

        return config_files
