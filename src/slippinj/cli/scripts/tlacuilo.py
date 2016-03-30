import os

from .basic_script import BasicScript


class Tlacuilo(BasicScript):
    """Compile the XML code for the workflows based on the given templates and configuration files"""

    def get_arguments(self):
        """
        Get the arguments to configure current script
        :return: list
        """
        return [
            {
                'short': '-w',
                'long': '--wf-dir',
                'help': 'Folder where all the workflows files are present',
                'required': True
            },
            {
                'short': '-t',
                'long': '--template-dir',
                'help': 'Folder where all the templates can be found, it should be the root folder inside them all the templates can be found',
                'required': True
            },
            {
                'short': '-o',
                'long': '--output-dir',
                'help': 'Directory where to store the compiled code'
            },
            {
                'short': '-e',
                'long': '--extra',
                'help': 'Extra variables to send to the templates',
                'action': 'append'
            },
            {
                'short': '-c',
                'long': '--configuration-file',
                'help': 'File where all the configuration is stored'
            },
            {
                'short': '-b',
                'long': '--hive-metastore-bucket',
                'help': 'Bucket where all data is saved',
                'default': False
            },
            {
                'short': '-f',
                'long': '--hdfs-deploy-folder',
                'help': 'Folder where all the code will be deployed on HDFS',
                'default': False
            },
            {
                'short': '-i',
                'long': '--cluster-information',
                'help': 'Try to get cluster information in order to replace variables in the template',
                'default': False
            }
        ]

    def run(self, args, injector):
        """
        Run the component to compile the XML workflows using the given templates and configuration files
        :param args: Namespace
        :param injector: Injector
        """
        logger = injector.get('logger')

        output_directory = args.output_dir if None != args.output_dir else injector.get(
            'filesystem').generate_temp_dir()

        if not os.path.isabs(output_directory):
            raise IOError('Output directory should be an absolute path in order to save the files')

        logger.info('Getting configuration from files')
        configuration = self.get_wf_configuration(args, injector)
        if args.cluster_information:
            for k, v in injector.get('emr_cluster').get_cluster_information(args.cluster_information).items():
                configuration[k] = v

        configuration.output_directory = output_directory

        if type(args.extra) == list:
            logger.info('Generating configuration from extra variables')
            for value in args.extra:
                value_splitted = value.split('=')
                if len(value_splitted) > 1:
                    configuration[value_splitted[0]] = value_splitted[1]
                else:
                    configuration[value] = ''

        logger.info('Rendering workflows code')
        injector.get('wf_templates_render').render_workflow_folder(
            args.template_dir,
            configuration.template,
            output_directory,
            configuration
        )

        if 'hive_template' in configuration:
            logger.info('Rendering hive templates')
            for table_type in ['incremental_tables', 'snapshot_tables', 'other_tables']:
                if table_type in configuration:
                    injector.get('hive_templates_render').render_hive_folder(
                        args.template_dir,
                        configuration['hive_template'],
                        os.path.join(output_directory, 'hive'),
                        configuration[table_type]
                    )
