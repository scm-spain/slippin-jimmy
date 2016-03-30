from injector import inject


class HDFSFilesystem(object):
    """Run HDFS commands inside the cluster"""

    @inject(emr_cluster='emr_cluster', logger='logger')
    def __init__(self, emr_cluster, logger):
        """
        Initialize the class
        :param emr_cluster: EMRCluster
        """
        super(HDFSFilesystem, self).__init__()
        self.__emr_cluster = emr_cluster
        self.__logger = logger

    def rmdir(self, path, cluster_id):
        self.__logger.debug('Removing {path} from cluster {cluster}'.format(path=path, cluster=cluster_id))
        return self.__emr_cluster.exec_command('hdfs dfs -rm -r -f ' + path, cluster_id)

    def mkdir(self, path, cluster_id):
        self.__logger.debug('Creating directory {path} in cluster {cluster}'.format(path=path, cluster=cluster_id))
        return self.__emr_cluster.exec_command('hdfs dfs -mkdir -p ' + path, cluster_id)

    def put(self, src, dest, cluster_id):
        self.__logger.debug(
            'Uploading {src} to {dest} in cluster {cluster}'.format(src=src, dest=dest, cluster=cluster_id))
        return self.__emr_cluster.exec_command('hdfs dfs -put ' + src + ' ' + dest, cluster_id)
