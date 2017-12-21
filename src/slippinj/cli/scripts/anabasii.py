import os

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
                'help': 'Provide a cluster id to work with, in case you don\'t provide one and didn\'t do it in Tlacuilo, a list of available clusters will be shown to select one',
                'default': False
            },
            {
                'short': '-d',
                'long': '--hdfs-deploy-folder',
                'help': 'Folder on HDFS to deploy the workflow',
                'default': False
            },
            {
                'short': '-w',
                'long': '--wf-dir',
                'help': 'Folder where all the workflows files are present',
                'required': True
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
        Run the component to upload the code to the cluster
        :param args: Namespace
        :param injector: Injector
        """
        logger = injector.get('logger')

        cluster_id = ''

        deploy_folder = args.hdfs_deploy_folder

        if args.script not in __name__:
            logger.info('Getting workflow configuration')
            configuration = self.get_wf_configuration(args, injector)
            if args.local_mode == False:
                if 'cluster_id' not in configuration:
                    configuration.cluster_id = args.cluster_id if False != args.cluster_id else injector.get('interactive_cluster_id').get()
                cluster_id = configuration.cluster_id
            if 'hdfs_deploy_folder' in configuration:
                deploy_folder = configuration.hdfs_deploy_folder
            wf_compiled_dir = configuration.output_directory if configuration.output_directory else args.wf_dir
        else:
            wf_compiled_dir = args.wf_dir
            if args.local_mode == False:
                cluster_id = args.cluster_id if False != args.cluster_id else injector.get('interactive_cluster_id').get()

        logger.info('Uploading {wf_dir} to the cluster {cluster_id}'.format(wf_dir=wf_compiled_dir, cluster_id=cluster_id))

        workflow_folder_name = 'workflow'
        if args.wf_dir:
            workflow_folder_name = args.wf_dir.strip(os.sep).split(os.sep)[-1]

        injector.get('emr_deploy').upload_code(wf_compiled_dir, cluster_id, deploy_folder, workflow_folder_name)
