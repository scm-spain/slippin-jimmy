from injector import inject


class ClusterId(object):
    """Get the cluster id interactively asking user in the CLI"""

    @inject(aws_emr_client='aws_emr_client')
    def __init__(self, aws_emr_client):
        """
        Initialize the class
        :param aws_emr_client: EMR.client
        """
        super(ClusterId, self).__init__()

        self.__aws_emr_client = aws_emr_client

    def get(self):
        """
        Ask the user to select one cluster from the currently active
        :return: string
        """
        print 'Cluster id has not been provided, getting the cluster currently active to select one... please be patient'
        cluster_list = self.__aws_emr_client.list_clusters(
            ClusterStates=['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING'])

        if not cluster_list['Clusters']:
            raise LookupError('There are not available cluster to upload the code')

        for index, cluster in enumerate(cluster_list['Clusters']):
            print '[{index}]\tCluster Name: {name}\tCluster Id: {id}'.format(index=index, name=cluster['Name'],
                                                                             id=cluster['Id'])

        index = int(raw_input('Select cluster to deploy in: '))
        if index > len(cluster_list['Clusters']):
            raise LookupError('Selected cluster not in list')

        return cluster_list['Clusters'][index]['Id']
