from .basic_script import BasicScript


class Valet(BasicScript):
    """Provision the cluster with the needed software"""

    def get_arguments(self):
        """
        Get the arguments to configure current script
        :return: list
        """
        return [
            {
                'short': '-p',
                'long': '--playbook',
                'help': 'Ansible playbook to execute in order to provision the cluster'
            },
            {
                'short': '-c',
                'long': '--cluster-id',
                'help': 'Cluster to execute the provisioning'
            },
            {
                'short': '-x',
                'long': '--create-cluster',
                'help': 'Configuration to launch a cluster on the given AWS profile'
            }
        ]

    def run(self, args, injector):
        """
        Run the component to provision the cluster using Ansible
        :param args: Namespace
        :param injector: Injector
        """
        if args.playbook:
            cluster_id = args.cluster_id if None != args.cluster_id else injector.get('interactive_cluster_id').get()

            injector.get('logger').info('Running provided playbook on the cluster')
            injector.get('ansible_client').run_playbook(args.playbook, cluster_id)
        elif args.create_cluster:
            injector.get('logger').info(
                'Launching cluster based on {cluster_config} configuration'.format(cluster_config=args.create_cluster))
            injector.get('job_flow').run_cluster(
                injector.get('yaml_configuration').read_config_file(args.create_cluster))
        else:
            raise RuntimeError('Not arguments where provided to run Valet')
