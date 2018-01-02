import os
import glob

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
                'help': 'Folder where all the workflows files are present'
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
                'short': '-i',
                'long': '--cluster-information',
                'action': 'store_true',
                'help': 'Ask interactively for cluster information in order to replace variables in the template',
                'default': False
            },
            {
                'short': '-l',
                'long': '--local-mode',
                'action': 'store_true',
                'help': 'If set, we assume that we\'re on the cluster and no remote connection needs to be made',
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
            cluster_id = injector.get('interactive_cluster_id').get()
            for k, v in injector.get('emr_cluster').get_cluster_information(cluster_id).items():
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

        logger.info('Checking for .py spark files on selected configuration folders')
        python_files = []
        for path in configuration.config_paths:
            root_path = os.path.dirname(path)
            current_path_files = glob.glob(os.path.join(root_path, '*.py'))
            python_files.extend(current_path_files)

        if python_files:
            logger.info('Copying .py spark files into tmp folder')
            injector.get('filesystem').mkdir(os.path.join(output_directory, 'lib/'))
            for py in python_files:
                injector.get('filesystem').cp(
                    py,
                    os.path.join(output_directory, 'lib/')
                )