from .basic_script import BasicScript


class Cooper(BasicScript):
    """Run the workflows once has been uploaded"""

    def get_arguments(self):
        """
        Get the arguments to configure current script
        :return: list
        """
        return [
            {
                'short': '-c',
                'long': '--cluster-id',
                'help': 'Provide a cluster id to work with, in case you don\'t provide one a list of available clusters will be shown to select one',
                'default': False
            },
            {
                'short': '-w',
                'long': '--wf-dir',
                'help': 'Folder where all the workflows files are present',
                'required': True
            }
        ]

    def run(self, args, injector):
        """
        Run the component to run the workflows in the cluster
        :param args: Namespace
        :param injector: Injector
        """
        configuration = self.get_wf_configuration(args, injector)
        wf_compiled_dir = configuration.output_directory if configuration.output_directory else args.wf_dir
        cluster_id = configuration.cluster_id if configuration.cluster_id else args.cluster_id

        properties_file = injector.get('interactive_properties_file').get(wf_compiled_dir)
        if properties_file:
            injector.get('logger').info(
                'Running {properties_file} in cluster {cluster_id}'.format(properties_file=properties_file,
                                                                           cluster_id=cluster_id))
            injector.get('emr_deploy').run_properties_file(properties_file, cluster_id)
