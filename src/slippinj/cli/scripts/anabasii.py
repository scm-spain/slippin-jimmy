import os

import sys

from .basic_script import BasicScript


class Anabasii(BasicScript):
    """Upload the compiled code to the cluster"""

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
                'short': '-m',
                'long': '--hive-metastore-bucket',
                'help': 'Bucket where the Hive tables are stored',
                'default': False
            },
            {
                'short': '-d',
                'long': '--hdfs-deploy-folder',
                'help': 'Folder on HDFS to deploy the code',
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
        Run the component to upload the code to the cluster
        :param args: Namespace
        :param injector: Injector
        """
        logger = injector.get('logger')
        cluster_id = args.cluster_id if False != args.cluster_id else injector.get('interactive_cluster_id').get()

        if args.script not in __name__:
            logger.info('Getting workflow configuration')
            configuration = self.get_wf_configuration(args, injector)
            configuration.cluster_id = cluster_id

            wf_compiled_dir = configuration.output_directory if configuration.output_directory else args.wf_dir
        else:
            wf_compiled_dir = args.wf_dir
            configuration = injector.get('interactive_default_configuration').get('devel', args, {})

        logger.info('Uploading {wf_dir} to the cluster {cluster_id}'.format(wf_dir=wf_compiled_dir, cluster_id=cluster_id))
        injector.get('emr_deploy').upload_code(wf_compiled_dir, cluster_id, configuration['hdfs_deploy_folder'],
                                               args.wf_dir.strip(os.sep).split(os.sep)[-1])
